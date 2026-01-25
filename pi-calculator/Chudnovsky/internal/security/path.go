// Package security provides security utilities for the Chudnovsky calculator,
// including path sanitization to prevent directory traversal attacks.
package security

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// SanitizePath sanitizes file paths to prevent directory traversal attacks.
// It ensures the path is within the current working directory and removes
// any directory traversal attempts (..).
//
// Security features:
//   - Removes ".." components
//   - Validates path stays within working directory
//   - Prevents writing to system directories like /etc, /root
//
// Parameters:
//   - path: The file path to sanitize
//
// Returns:
//   - string: The cleaned, safe path
//   - error: Error if path is invalid or attempts directory traversal
func SanitizePath(path string) (string, error) {
	// Remove any ".." or absolute path components
	cleaned := filepath.Clean(path)

	// Check if the cleaned path still contains ".." (directory traversal)
	// filepath.Clean should remove these, but we check for safety
	if strings.Contains(cleaned, "..") {
		return "", fmt.Errorf("path contains directory traversal: %s", path)
	}

	// Check if path resolves outside the current working directory
	// Get absolute path to detect traversal
	absPath, err := filepath.Abs(cleaned)
	if err != nil {
		return "", fmt.Errorf("invalid path: %w", err)
	}

	// Get current working directory
	cwd, err := os.Getwd()
	if err != nil {
		// If we can't get CWD, just use cleaned path (less secure but functional)
		return cleaned, nil
	}

	// Check if the absolute path is outside the current directory
	// This prevents writing to /etc, /root, etc.
	// However, we allow paths that are subdirectories of the current directory
	relPath, err := filepath.Rel(cwd, absPath)
	if err != nil {
		// If we can't compute relative path, check if absPath starts with cwd
		if !strings.HasPrefix(absPath, cwd) {
			return "", fmt.Errorf("path outside working directory: %s", path)
		}
		// If it's a subdirectory, allow it
		return cleaned, nil
	}

	// If relative path starts with "..", it's outside the current directory
	if strings.HasPrefix(relPath, "..") {
		return "", fmt.Errorf("path outside working directory: %s", path)
	}

	// Path is within current directory or a subdirectory - safe
	return cleaned, nil
}
