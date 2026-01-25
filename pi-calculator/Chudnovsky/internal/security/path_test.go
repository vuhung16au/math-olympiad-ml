package security

import (
	"os"
	"path/filepath"
	"testing"
)

func TestSanitizePath_Package(t *testing.T) {
	result, err := SanitizePath("results/test.txt")
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if result == "" {
		t.Error("Expected non-empty result")
	}

	// Test directory traversal rejection
	_, err = SanitizePath("../../../etc/passwd")
	if err == nil {
		t.Error("Expected error for directory traversal")
	}
}

func TestSanitizePath_EdgeCases(t *testing.T) {
	// Test empty path
	_, err := SanitizePath("")
	if err != nil {
		t.Logf("Empty path error (may be expected): %v", err)
	}

	// Test absolute path in current directory
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("Failed to get working directory: %v", err)
	}
	absPath := filepath.Join(cwd, "test.txt")
	result, err := SanitizePath(absPath)
	if err != nil {
		t.Errorf("Expected no error for path in current directory: %v", err)
	}
	if result == "" {
		t.Error("Expected non-empty result")
	}

	// Test relative path with normalization
	_, err = SanitizePath("results/../test.txt")
	if err != nil {
		t.Errorf("Expected normalized path to work: %v", err)
	}
}
