#[macro_use]
extern crate lazy_static;
use anyhow::Context;
use anyhow::bail;
use pyo3::exceptions;
use pyo3::prelude::*;
use std::borrow::Cow;
use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{prelude::*, BufReader};
use std::path::Path;

lazy_static! {
    static ref ALPHABET: HashSet<char> = HashSet::from([
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
        's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ]);
}

#[derive(Clone, Copy)]
enum CleanOption {
    Standard,
    LowerOnly,
}

impl CleanOption {
    #[inline]
    fn clean(self, text: String) -> String {
        // Return `text` lower-cased with non-alphanumeric characters removed.
        let mut text_lower = text.to_lowercase();
        match self {
            CleanOption::Standard => {
                text_lower.retain(|b: char| ALPHABET.contains(&b));
            }
            _ => {}
        };
        text_lower
    }
}
impl FromPyObject<'_> for CleanOption {
    fn extract(ob: &'_ PyAny) -> PyResult<Self> {
        let val = match String::extract(ob) {
            Ok(s) => match s.as_str() {
                "standard" => CleanOption::Standard,
                "lower_only" => CleanOption::LowerOnly,
                _ => {
                    return Err(exceptions::PyValueError::new_err(format!(
                        "unknown clean_option: {}",
                        s.as_str()
                    )));
                }
            },
            Err(err) => return Err(exceptions::PyValueError::new_err(err)),
        };
        Ok(val)
    }
}

fn parse_bigram_borrowed(s: &str) -> anyhow::Result<[Cow<'_, str>; 2]> {
    let mut words = s.split(' ');
    let w1 = words.next();
    let w2 = words.next();
    let w3 = words.next();
    match (w1, w2, w3) {
        (Some(w1), Some(w2), None) => Ok([w1.into(), w2.into()]),
        _ => bail!("invalid bigram"),
    }
}

fn parse_bigram_owned(s: &str) -> anyhow::Result<[Cow<'static, str>; 2]> {
    let mut words = s.split(' ');
    let w1 = words.next();
    let w2 = words.next();
    let w3 = words.next();
    match (w1, w2, w3) {
        (Some(w1), Some(w2), None) => Ok([w1.to_owned().into(), w2.to_owned().into()]),
        _ => bail!("invalid bigram"),
    }
}

#[pyclass(subclass)]
struct Segmenter {
    basepath: String,
    unigrams: HashMap<String, f64>,
    bigrams: HashMap<[Cow<'static, str>; 2], f64>,
    #[pyo3(set)]
    cleaner: CleanOption,

    #[pyo3(get, set)]
    limit: usize,
    #[pyo3(get, set)]
    total: f64,
}

struct Searcher<'a> {
    unigrams: &'a HashMap<String, f64>,
    bigrams: &'a HashMap<[Cow<'static, str>; 2], f64>,
    limit: usize,
    total: f64,
    memo: HashMap<(&'a str, &'a str), (f64, Vec<&'a str>)>,
}

impl<'a> Searcher<'a> {
    fn new(
        unigrams: &'a HashMap<String, f64>,
        bigrams: &'a HashMap<[Cow<'static, str>; 2], f64>,
        limit: usize,
        total: f64,
    ) -> Self {
        let memo: HashMap<(&'a str, &'a str), (f64, Vec<&'a str>)> = HashMap::new();
        Searcher {
            unigrams: unigrams,
            bigrams: bigrams,
            limit: limit,
            total: total,
            memo: memo,
        }
    }

    fn divide(&self, text: &'a str) -> impl Iterator<Item = (&'a str, &'a str)> {
        // Yield `(prefix, suffix)` pairs from `text`.
        let end = std::cmp::min(text.len(), self.limit) + 1;
        (1..end).map(|pos| (&text[..pos], &text[pos..]))
    }

    fn score(&self, word: &str, previous: Option<&str>) -> f64 {
        let prev = match previous {
            Some(p) => p,
            None => {
                if let Some(v) = self.unigrams.get(word) {
                    return v / self.total;
                }

                // Penalize words not found in the unigrams according
                // to their length, a crucial heuristic.

                return 10.0 / (self.total * 10.0_f64.powf(word.len() as f64));
            }
        };

        let bigram: [Cow<str>; 2] = [prev.into(), word.into()];
        let bigram_res = self.bigrams.get(&bigram);
        if let Some(bigram_res) = bigram_res {
            if self.unigrams.get(prev).is_some() {
                // Conditional probability of the word given the previous
                // word. The technical name is *stupid backoff* and it's
                // not a probability distribution but it works well in
                // practice.
                return bigram_res / self.total / self.score(prev, None);
            }
        }
        // Fall back to using the unigram probability.
        self.score(word, None)
    }

    fn search(&mut self, text: &'a str, previous: Option<&str>) -> (f64, Vec<&'a str>) {
        // Return max of candidates matching `text` given `previous` word.
        if text.is_empty() {
            return (0.0, Vec::new());
        }

        let previous = previous.unwrap_or("<s>");

        let divided = self.divide(text);
        let mut max_candidate_value: f64 = f64::NEG_INFINITY;
        let mut max_candidate: Vec<&str> = Vec::new();
        for (prefix, suffix) in divided {
            let prefix_score = self.score(prefix, Some(previous)).log10();
            let pair = (suffix, prefix);

            if !self.memo.contains_key(&pair) {
                let r = self.search(suffix, Some(prefix));
                self.memo.insert(pair, r);
            }
            let (suffix_score, suffix_words) = &self.memo[&pair];

            let candidate_score = prefix_score + suffix_score;
            if candidate_score > max_candidate_value {
                max_candidate_value = candidate_score;

                let mut candidate = vec![prefix];
                candidate.extend(suffix_words);
                max_candidate = candidate;
            }
        }
        (max_candidate_value, max_candidate)
    }
}

// rust methods
impl Segmenter {
    fn py_load(&mut self, basepath: &str) -> anyhow::Result<()> {
        let path = Path::new(basepath);
        self.unigrams = self.parse_unigrams(path.join("unigrams.txt").to_str().context("")?)?;
        self.bigrams = self.parse_bigrams(path.join("bigrams.txt").to_str().context("")?)?;
        Ok(())
    }

    fn parse_unigrams(&mut self, filename: &str) -> anyhow::Result<HashMap<String, f64>> {
        let file = File::open(filename)?;
        let reader = BufReader::new(file);
        let mut result: HashMap<String, f64> = HashMap::new();
        for line in reader.lines() {
            let mut line = line?;
            if line.is_empty() {
                continue;
            }
            let mut words = line.split('\t');
            let word = words.next();
            let score = words.next();
            if let (Some(word), Some(score)) = (word, score) {
                let score = score.parse::<f64>()?;
                let wordlen = word.len();
                line.truncate(wordlen);
                result.insert(line, score);
            }
        }
        Ok(result)
    }

    fn parse_bigrams(&mut self, filename: &str) -> anyhow::Result<HashMap<[Cow<'static, str>; 2], f64>> {
        let file = File::open(filename)?;
        let reader = BufReader::new(file);
        let mut result: HashMap<[Cow<str>; 2], f64> = HashMap::new();
        for line in reader.lines() {
            let line = line?;
            if line.is_empty() {
                continue;
            }
            let mut words = line.split('\t');
            let bigram = words.next();
            let score = words.next();
            if let (Some(bigram), Some(score)) = (bigram, score) {
                let score = score.parse::<f64>()?;
                let bigram = parse_bigram_owned(bigram)?;
                result.insert(bigram, score);
            }
        }
        Ok(result)
    }

    fn clean(&self, text: String) -> String {
        // Return `text` lower-cased with non-alphanumeric characters removed.
        self.cleaner.clean(text)
    }

    fn do_segment(&self, text: String) -> Vec<String> {
        let mut output: Vec<String> = Vec::new();

        let mut s = Searcher::new(&self.unigrams, &self.bigrams, self.limit, self.total);

        let clean_text = self.clean(text);
        let size = 250;
        let mut prefix_len = 0;

        for offset in (0..clean_text.len()).step_by(size) {
            let max_ = std::cmp::min(clean_text.len(), offset + size);
            let chunk: &str = &clean_text[offset - prefix_len..max_];
            let (_, chunk_words) = s.search(chunk, None);
            let len = chunk_words.len();
            let last_5 = &chunk_words[len.saturating_sub(5)..];
            prefix_len = last_5.iter().map(|word| word.len()).sum();
            for word in &chunk_words[..len.saturating_sub(5)] {
                output.push(word.to_string());
            }
        }
        let (_, prefix_words) = s.search(&clean_text[clean_text.len() - prefix_len..], None);

        for word in prefix_words {
            output.push(word.to_string());
        }
        output
    }
}

#[pymethods]
impl Segmenter {
    #[new]
    #[args(limit = "24")]
    fn new(basepath: &str, limit: usize) -> Self {
        Segmenter {
            basepath: basepath.to_string(),
            unigrams: HashMap::new(),
            bigrams: HashMap::new(),
            limit,
            total: 0.0,
            cleaner: CleanOption::Standard,
        }
    }

    #[getter]
    fn cleaner(&self) -> PyResult<String> {
        let v = match self.cleaner {
            CleanOption::Standard => "standard".to_string(),
            CleanOption::LowerOnly => "lower_only".to_string(),
        };
        Ok(v)
    }

    fn get_unigram(&mut self, key: String, default: f64) -> PyResult<f64> {
        Ok(*self.unigrams.get(&key).unwrap_or(&default))
    }

    fn get_bigram(&mut self, key: String, default: f64) -> PyResult<f64> {
        let bigram = parse_bigram_borrowed(&key)?;
        Ok(*self.bigrams.get(&bigram).unwrap_or(&default))
    }

    fn load(&mut self) -> PyResult<()> {
        self.py_load(&self.basepath.clone())?;
        self.total = 1024908267229.0;
        Ok(())
    }

    fn segment(&mut self, word: String) -> PyResult<Vec<String>> {
        let res = self.do_segment(word);
        Ok(res)
    }

    fn add_unigram(&mut self, key: String, value: f64) -> PyResult<()> {
        self.unigrams.insert(key, value);
        Ok(())
    }

    fn add_bigram(&mut self, key: String, value: f64) -> PyResult<()> {
        let bigram = parse_bigram_owned(&key)?;
        self.bigrams.insert(bigram, value);
        Ok(())
    }
}
/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name = "wordsegment_rs")]
fn python_wordsegment(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Segmenter>()?;
    Ok(())
}
