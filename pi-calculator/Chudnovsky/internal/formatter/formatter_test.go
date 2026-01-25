package formatter

import (
	"strings"
	"testing"
)

func TestFormatPiOutput_Package(t *testing.T) {
	output := FormatPiOutput(10, "3.1415926535")
	if !strings.Contains(output, "10 Digits of Pi") {
		t.Error("Expected '10 Digits of Pi' in output")
	}
}

func TestFormatPiOutput_EdgeCases(t *testing.T) {
	// Test empty string
	output := FormatPiOutput(0, "")
	if output == "" {
		t.Error("Expected non-empty output")
	}

	// Test single digit
	output = FormatPiOutput(1, "3")
	if !strings.Contains(output, "3") {
		t.Error("Expected '3' in output")
	}

	// Test thousand
	output = FormatPiOutput(1000, "3.14")
	if !strings.Contains(output, "Thousand") {
		t.Error("Expected 'Thousand' in output")
	}

	// Test million
	output = FormatPiOutput(1000000, "3.14")
	if !strings.Contains(output, "Million") {
		t.Error("Expected 'Million' in output")
	}

	// Test digits grouping
	piStr := "3." + strings.Repeat("1", 150)
	output = FormatPiOutput(150, piStr)
	lines := strings.Split(output, "\n")
	digitLineCount := 0
	for _, line := range lines {
		if len(line) == 50 {
			digitLineCount++
		}
	}
	if digitLineCount < 3 {
		t.Errorf("Expected at least 3 lines of 50 digits, got %d", digitLineCount)
	}
}
