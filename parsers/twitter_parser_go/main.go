package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path"
    twitterscraper "github.com/n0madic/twitter-scraper"
)

func main() {
	// Create a new Scraper
	s := twitterscraper.New()
	s.WithDelay(5)


	// Open the CSV file
	f, err := os.Open("file.csv")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer f.Close()

	// Read the CSV file
	lines, err := csv.NewReader(f).ReadAll()
	if err != nil {
		fmt.Println(err)
		return
	}

	// Loop through each line (Twitter handle)
	for i, line := range lines {
		if i == 0 {
			// Append "Twitter followers" to the first line
			lines[i] = append(line, "Twitter Followers")
			continue
		}
		
		// Assuming the handle is the first column
		url := line[4]
		handle := path.Base(url)

		// Print the line number and Twitter handle
		fmt.Printf("Processing line %d: @%s\n", i+1, handle)
	
		// Get the user's profile
		profile, err := s.GetProfile(handle)
		if err != nil {
			fmt.Println(err)
			continue
		}
	
		// Append the number of followers to the line
		lines[i] = append(line, fmt.Sprintf("%d", profile.FollowersCount))
	}

	// Open the CSV file with write permissions
	f, err = os.Create("file.csv")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer f.Close()

	// Write the lines back to the CSV file
	w := csv.NewWriter(f)
	w.WriteAll(lines)
	if err := w.Error(); err != nil {
		fmt.Println(err)
	}
}