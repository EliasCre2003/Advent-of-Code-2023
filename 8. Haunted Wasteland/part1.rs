use std::collections::HashMap;
use std::fs::File;
use std::io::prelude::*;

struct LR {
    left: String,
    right: String
}

fn get_lines(file_path: &str) -> Vec<String> {
    let mut file = File::open(file_path).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    contents
        .split('\n')
        .map(|s| s.to_string()
                .replace('\n', "")
                .replace('\r', "")
        )
        .collect()
}

fn create_node_map(lines: Vec<String>) -> HashMap<String, LR> {
    let mut map = HashMap::new();
    for line in lines.into_iter() {
        let key = (&line[0..3]).to_string();
        let val = LR{
            left:  (&line[7..10]).to_string(),
            right: (&line[12..15]).to_string(),
        };
        map.insert(key, val);
    }
    map

}

fn main() {
    let lines = get_lines("input.txt");
    let lr_sequence: Vec<char> = lines.get(0).unwrap().chars().collect();
    let node_map = create_node_map(lines[2..].to_vec());
    let mut count: u64 = 0;
    let mut current_key = &String::from("AAA");
    while current_key != "ZZZ" {
        let lr = lr_sequence.get((count % lr_sequence.len() as u64) as usize).unwrap();
        let instruction = node_map.get(current_key).unwrap();
        current_key = match lr {
            'R' => &instruction.right,
            'L' => &instruction.left,
            _ => panic!("Unexpected character: {}", lr)
        };
        count += 1;
    }

    println!("{}", count)

}