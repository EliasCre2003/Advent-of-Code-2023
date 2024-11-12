use std::fs::File;
use std::io::prelude::*;

struct Conversion {
    source: u64,
    destination: u64,
    size: u64,
}

impl Conversion {
    fn convert(&self, input: u64) -> u64 {
        if !self.is_inside(input) {
            input
        } else {
            input + self.destination - self.source
        }
    }

    fn is_inside(&self, input: u64) -> bool {
        return input >= self.source && input < self.source + self.size
    }
}

struct ConversionMap {
    conversions: Vec<Conversion>,
}

impl ConversionMap {
    fn convert(&self, input: u64) -> u64 {
        for conversion in &self.conversions {
            if conversion.is_inside(input) {
                return conversion.convert(input);
            }
        };
        input
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
    let mut seed_nums: Vec<&str> = seed_line.split(" ").collect();
    seed_nums.remove(0);
    let seed_nums: Vec<u64> = seed_nums
        .into_iter()
        .map(|s| u64::from_str_radix(s, 10).unwrap())
        .collect();
    let mut seed_ranges: Vec<(u64, u64)> = Vec::new();
    let mut i: usize = 0;
    while i < seed_nums.len() - 1 {
        seed_ranges.push((seed_nums.get(i).unwrap().to_owned(), seed_nums.get(i + 1).unwrap().to_owned()));
        i += 1;
    };
    seed_ranges
}

fn get_conversion_maps(mut lines: Vec<String>) -> Vec<ConversionMap> {
    lines.remove(0); lines.remove(0);
    let mut map_lines: Vec<Vec<String>> = Vec::new();
    let mut current_map_lines = Vec::new();
    for line in lines {
        if line.len() == 0 && current_map_lines.len() > 0 {
            map_lines.push(current_map_lines);
            current_map_lines = Vec::new();
        }
        else if ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'].contains(&line.chars().nth(0).unwrap()) {
            current_map_lines.push(line);
        }
    };
    let mut conversion_maps: Vec<ConversionMap> = Vec::new();
    for lines in map_lines {
        let mut map: Vec<Conversion> = Vec::new();
        // map = lines
        //     .into_iter()
        //     .map(|conversion| {
        //             let vals = conversion
        //                 .split(" ")
        //                 .collect()
        //                 .map(|s| u64::from_str_radix(s, 10).unwrap())
        //                 .to
        //             Conversion {
        //                 source: vals
        //             }
        //         }
        //     )
        for conversion in lines {
            let vals: Vec<u64> = conversion
                .split(" ")
                .map(|s| u64::from_str_radix(s, 10).unwrap())
                .collect();
            map.push(Conversion {
                source: vals.get(1).unwrap().to_owned(),
                destination: vals.get(0).unwrap().to_owned(),
                size: vals.get(2).unwrap().to_owned()
            });
        }
        conversion_maps.push(ConversionMap{conversions: map});
    }
    conversion_maps
}


// fn 

fn main() {
    
    let lines = get_lines("test.txt");
    let seed_ranges = get_seed_ranges(lines.get(0).unwrap());
    println!("Range done");
    let conversion_maps = get_conversion_maps(lines);
    let mut min = u64::max_value();

    println!("{}", seed_ranges.get(0).unwrap().1);
    
    for (i, range) in seed_ranges.iter().enumerate() {
        for (j, seed) in (range.0..(range.0+range.1)).enumerate() {
            let mut value = seed;
            for map in &conversion_maps {
                value = map.convert(value);
            }
            if value < min {
                min = value;
            }
            if (j % 1000000) == 0 {
                println!("Did {} million", j)
            }

        }
        println!("Did {} ranges", i)
    }


    println!("{}", min)

}
