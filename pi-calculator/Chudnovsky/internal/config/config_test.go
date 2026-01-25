package config

import "testing"

func TestDefault(t *testing.T) {
	cfg := Default()
	if cfg == nil {
		t.Fatal("Expected non-nil config")
	}

	if cfg.MaxDigits <= 0 {
		t.Error("Expected positive MaxDigits")
	}

	if cfg.DigitsPerTerm <= 0 {
		t.Error("Expected positive DigitsPerTerm")
	}

	if cfg.BitsPerDigit <= 0 {
		t.Error("Expected positive BitsPerDigit")
	}
}
