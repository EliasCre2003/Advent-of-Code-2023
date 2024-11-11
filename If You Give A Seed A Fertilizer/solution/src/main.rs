use std::fs::File;
use std::io::prelude::*;

struct Conversion {
    source: u64,
    destination: u64,
    size: u64,
}

impl Conversion {
    fn convert(&self, input: u64) -> u64 {
        if input < self.source || input > self.source + self.size {
            input
        } else {
            input + self.destination - self.source
        }
    }
}

fn get_lines(file_path: &str) -> Vec<String> {
    let mut file = File::open(file_path).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    contents
        .split('\n')
        .map(|s| s.to_string().replace('\n', "").replace('\r', ""))
        .collect()
}

fn get_seed_ranges(seed_line: &String) -> Vec<(u64, u64)> {
    let seed_nums: Vec<&str> = seed_line.split(" ").collect();
    seed_nums.remove(0);
    let seed_nums: Vec<u64> = seed_nums
        .into_iter()
        .map(|s| u64::from_str_radix(s, 10).unwrap())
        .collect();

    let seed_ranges = Vec::new();
    let i: usize = 0;
    while i < seed_nums.len() - 1 {
        seed_ranges.append((seed_nums.get(i), seed_nums.get(i + 1)));
    }
}

struct ConversionMap {
    conversions: Vec<Conversion>,
}

fn main() {
    let lines = get_lines("input.txt");
    let seed_line = lines.get(0).unwrap();
}
