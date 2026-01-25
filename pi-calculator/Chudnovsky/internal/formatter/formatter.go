// Package formatter provides utilities for formatting π (pi) output
// in a human-readable format matching the project's standard format.
package formatter

import (
	"fmt"
	"strings"
)

// FormatPiOutput formats the pi string to match the correct-pi format.
// It creates a human-readable format with headers, attribution, and
// digits grouped in lines of 50 characters.
//
// The output format includes:
//   - Header with digit count (e.g., "1000 Digits of Pi")
//   - Attribution line
//   - GitHub repository URL
//   - "3." on its own line
//   - Subsequent digits in groups of 50 per line
//
// Parameters:
//   - digits: The number of digits being formatted
//   - piStr: The pi string (e.g., "3.14159...")
//
// Returns the formatted string with headers and properly grouped digits.
func FormatPiOutput(digits int, piStr string) string {
	var result strings.Builder

	// Format number of digits with proper suffix
	var digitLabel string
	switch {
	case digits >= 1000000 && digits%1000000 == 0:
		digitLabel = fmt.Sprintf("%d Million Digits of Pi", digits/1000000)
	case digits >= 1000 && digits%1000 == 0:
		digitLabel = fmt.Sprintf("%d Thousand Digits of Pi", digits/1000)
	default:
		digitLabel = fmt.Sprintf("%d Digits of Pi", digits)
	}

	// Write header
	result.WriteString(digitLabel + "\n")
	result.WriteString("collected by Vu Hung\n")
	result.WriteString("https://github.com/vuhung16au/math-olympiad-ml/tree/main/pi-calculator/Chudnovsky\n")
	result.WriteString("\n")

	// Extract digits after decimal point
	digitsAfterDecimal := piStr
	if strings.Contains(piStr, ".") {
		parts := strings.Split(piStr, ".")
		if len(parts) == 2 {
			result.WriteString("3.\n")
			digitsAfterDecimal = parts[1]
		} else {
			// Security: Bounds check before string slicing
			if len(piStr) >= 2 {
				result.WriteString(piStr[:2] + "\n")
				digitsAfterDecimal = piStr[2:]
			} else {
				result.WriteString(piStr + "\n")
				return result.String()
			}
		}
	} else {
		// If no decimal point, assume it starts with "3"
		if len(piStr) > 0 && piStr[0] == '3' {
			result.WriteString("3.\n")
			digitsAfterDecimal = piStr[1:]
		} else {
			result.WriteString(piStr + "\n")
			return result.String()
		}
	}

	// Format digits in groups of 50 per line
	// Security: Bounds are already checked in the loop condition and end calculation
	digitsPerLine := 50
	for i := 0; i < len(digitsAfterDecimal); i += digitsPerLine {
		end := i + digitsPerLine
		if end > len(digitsAfterDecimal) {
			end = len(digitsAfterDecimal)
		}
		// Additional safety check (though already ensured by condition above)
		if i < len(digitsAfterDecimal) && end <= len(digitsAfterDecimal) {
			result.WriteString(digitsAfterDecimal[i:end] + "\n")
		}
	}

	return result.String()
}
