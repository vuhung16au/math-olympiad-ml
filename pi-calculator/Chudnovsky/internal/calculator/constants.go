package calculator

import "math/big"

// Constants for Chudnovsky algorithm
var (
	// A is the constant 13591409 in the Chudnovsky formula
	A = big.NewInt(13591409)

	// B is the constant 545140134 in the Chudnovsky formula
	B = big.NewInt(545140134)

	// C is the constant 640320 in the Chudnovsky formula
	C = big.NewInt(640320)

	// C3 is C^3 = 640320^3, precomputed for efficiency
	C3 = new(big.Int).Exp(big.NewInt(640320), big.NewInt(3), nil)
)
