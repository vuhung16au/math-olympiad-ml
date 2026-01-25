package main

import (
	"fmt"
	"os"
	"strings"
)

// extractDigitsFromFile extracts just the digits from a pi file, handling both formats:
// 1. New format with headers: "XXX Digits of Pi\ncollected by...\n3.\n14159..."
// 2. Old format: just digits starting with "3.14159..." or "14159..."
func extractDigitsFromFile(content string) string {
	lines := strings.Split(content, "\n")
	
	// Find the line with "3." (exactly "3." on its own line)
	digitsStart := -1
	for i, line := range lines {
		line = strings.TrimSpace(line)
		if line == "3." {
			// Found "3." line, digits start on next line
			if i+1 < len(lines) {
				digitsStart = i + 1
				break
			}
		}
	}
	
	// If we found "3." line, collect digits from next lines
	if digitsStart >= 0 {
		var digits strings.Builder
		for i := digitsStart; i < len(lines); i++ {
			line := strings.TrimSpace(lines[i])
			if len(line) == 0 {
				continue // Skip empty lines
			}
			// Collect only digits from this line
			for _, r := range line {
				if r >= '0' && r <= '9' {
					digits.WriteRune(r)
				}
			}
		}
		return digits.String()
	}
	
	// Fallback: look for lines starting with digits (old format)
	for i, line := range lines {
		line = strings.TrimSpace(line)
		if len(line) > 0 && line[0] >= '0' && line[0] <= '9' {
			// Found a line starting with digits
			var digits strings.Builder
			// Check if it starts with "3."
			if strings.HasPrefix(line, "3.") {
				line = line[2:] // Remove "3." prefix
			} else if strings.HasPrefix(line, "3") && len(line) > 1 {
				line = line[1:] // Remove "3" prefix
			}
			// Collect all digit lines from here
			for j := i; j < len(lines); j++ {
				digLine := strings.TrimSpace(lines[j])
				if len(digLine) == 0 {
					continue
				}
				// Remove any non-digit characters
				for _, r := range digLine {
					if r >= '0' && r <= '9' {
						digits.WriteRune(r)
					}
				}
			}
			return digits.String()
		}
	}
	
	// Last fallback: extract all digits from content
	var digits strings.Builder
	for _, r := range content {
		if r >= '0' && r <= '9' {
			digits.WriteRune(r)
		}
	}
	result := digits.String()
	
	// Remove "3" prefix if present (for old format)
	if strings.HasPrefix(result, "3") {
		result = result[1:]
	}
	
	return result
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: go run compare_pi.go <calculated_file> <correct_file> [digits]")
		fmt.Println("  calculated_file: Path to the calculated pi file")
		fmt.Println("  correct_file: Path to the correct pi file")
		fmt.Println("  digits: Optional number of digits to compare (default: all)")
		os.Exit(1)
	}

	calculatedFile := os.Args[1]
	correctFile := os.Args[2]
	
	var maxDigits int = -1
	if len(os.Args) >= 4 {
		_, err := fmt.Sscanf(os.Args[3], "%d", &maxDigits)
		if err != nil {
			fmt.Printf("Error parsing digits: %v\n", err)
			os.Exit(1)
		}
	}

	// Read calculated pi
	calculatedBytes, err := os.ReadFile(calculatedFile)
	if err != nil {
		fmt.Printf("Error reading calculated file: %v\n", err)
		os.Exit(1)
	}
	calculated := extractDigitsFromFile(string(calculatedBytes))

	// Read correct pi
	correctBytes, err := os.ReadFile(correctFile)
	if err != nil {
		fmt.Printf("Error reading correct file: %v\n", err)
		os.Exit(1)
	}
	correct := extractDigitsFromFile(string(correctBytes))

	// Limit comparison to maxDigits if specified
	if maxDigits > 0 {
		if len(calculated) > maxDigits {
			calculated = calculated[:maxDigits]
		}
		if len(correct) > maxDigits {
			correct = correct[:maxDigits]
		}
	}

	// Compare (ignore last 2 digits due to rounding propagation)
	minLen := len(calculated)
	if len(correct) < minLen {
		minLen = len(correct)
	}

	// Compare up to third-to-last digit (ignore last 2 digits for rounding tolerance)
	compareLen := minLen
	if compareLen > 2 {
		compareLen = compareLen - 2 // Ignore last 2 digits for rounding tolerance
	} else if compareLen > 1 {
		compareLen = compareLen - 1 // If only 2 digits, ignore just the last one
	}

	matchCount := 0
	firstMismatch := -1
	
	for i := 0; i < compareLen; i++ {
		if calculated[i] == correct[i] {
			matchCount++
		} else if firstMismatch == -1 {
			firstMismatch = i
		}
	}
	
	// Check last 2 digits separately (for informational purposes only)
	lastDigitsDiff := false
	if minLen >= 2 && len(calculated) >= 2 && len(correct) >= 2 {
		if calculated[minLen-2:] != correct[minLen-2:] {
			lastDigitsDiff = true
		}
	} else if minLen >= 1 && len(calculated) >= 1 && len(correct) >= 1 {
		if calculated[minLen-1] != correct[minLen-1] {
			lastDigitsDiff = true
		}
	}

	// Print results
	fmt.Printf("Comparison Results:\n")
	fmt.Printf("  Calculated file: %s\n", calculatedFile)
	fmt.Printf("  Correct file:    %s\n", correctFile)
	fmt.Printf("  Calculated length: %d digits\n", len(calculated))
	fmt.Printf("  Correct length:    %d digits\n", len(correct))
	fmt.Printf("  Compared:          %d digits (last 2 digits ignored for rounding tolerance)\n", compareLen)
	fmt.Printf("  Matches:            %d digits\n", matchCount)
	
	if compareLen > 0 {
		accuracy := float64(matchCount) / float64(compareLen) * 100.0
		fmt.Printf("  Accuracy:          %.2f%%\n", accuracy)
	}
	
	// Note about last digits if different
	if lastDigitsDiff && minLen >= 2 {
		last2Calc := calculated[minLen-2:]
		last2Corr := correct[minLen-2:]
		fmt.Printf("  Note: Last 2 digits differ (acceptable rounding): calculated=%s, correct=%s\n", 
			last2Calc, last2Corr)
	} else if lastDigitsDiff && minLen >= 1 {
		fmt.Printf("  Note: Last digit differs (acceptable rounding): calculated=%c, correct=%c\n", 
			calculated[minLen-1], correct[minLen-1])
	}

	if firstMismatch >= 0 {
		// Mismatch found in non-last digits - this is an error
		fmt.Printf("\n  ✗ First mismatch at position %d (after decimal point):\n", firstMismatch+1)
		start := firstMismatch - 10
		if start < 0 {
			start = 0
		}
		end := firstMismatch + 10
		if end > len(calculated) {
			end = len(calculated)
		}
		if end > len(correct) {
			end = len(correct)
		}
		
		fmt.Printf("    Calculated: %c\n", calculated[firstMismatch])
		fmt.Printf("    Correct:    %c\n", correct[firstMismatch])
		fmt.Printf("    Context:    ...%s...\n", calculated[start:end])
		fmt.Printf("    Context:    ...%s...\n", correct[start:end])
		
		// Show last few digits if mismatch is near the end
		if firstMismatch >= compareLen-20 {
			fmt.Printf("\n  Last 20 digits:\n")
			lastStart := minLen - 20
			if lastStart < 0 {
				lastStart = 0
			}
			fmt.Printf("    Calculated: ...%s\n", calculated[lastStart:])
			fmt.Printf("    Correct:    ...%s\n", correct[lastStart:])
		}
		
		os.Exit(1)
	} else {
		// All compared digits match (last digit was ignored)
		if len(calculated) != len(correct) {
			fmt.Printf("\n  ⚠ Length mismatch: calculated has %d digits, correct has %d digits\n", 
				len(calculated), len(correct))
			os.Exit(1)
		} else {
			fmt.Printf("\n  ✓ Perfect match! All %d digits are correct (last 2 digits ignored for rounding).\n", matchCount)
			os.Exit(0)
		}
	}
}
