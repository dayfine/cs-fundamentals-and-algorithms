package kata_test

import (
	. "codewarrior/kata"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

func test(in, out, desc string) {
	Expect(Diff(in)).To(Equal(out), desc)
}

var _ = Describe("Sample Tests", func() {
	It("should pass simple tests", func() {
		test("5", "0", "constant should return 0")
		test("x", "1", "x should return 1")
		test("(+ x x)", "2", "x+x should return 2")
		test("(- x x)", "0", "x-x should return 0")
		test("(* x 2)", "2", "2*x should return 2")
		test("(/ x 2)", "0.5", "x/2 should return 0.5")
		test("(^ x 2)", "(* 2 x)", "x^2 should return 2*x")
		test("(cos x)", "(* -1 (sin x))", "cos(x) should return -1 * sin(x)")
		test("(sin x)", "(cos x)", "sin(x) should return cos(x)")
		test("(tan x)", "(+ 1 (^ (tan x) 2))", "tan(x) should return 1 + tan(x)^2")
		test("(exp x)", "(exp x)", "exp(x) should return exp(x)")
		test("(ln x)", "(/ 1 x)", "ln(x) should return 1/x")
	})

	It("should handle nested expressions", func() {
		test("(+ x (+ x x))", "3", "x+(x+x) should return 3")
		test("(- (+ x x) x)", "1", "(x+x)-x should return 1")
		test("(* 2 (+ x 2))", "2", "2*(x+2) should return 2")
		test("(/ 2 (+ 1 x))", "(/ -2 (^ (+ 1 x) 2))", "2/(1+x) should return -2/(1+x)^2")
		test("(cos (+ x 1))", "(* -1 (sin (+ x 1)))", "cos(x+1) should return -1 * sin(x+1)")

		// Accepting (* 2 (* -1 (sin (* 2 x)))) or (* -2 (sin (* 2 x)))
		Expect(Diff("(cos (* 2 x))")).To(Or(Equal("(* 2 (* -1 (sin (* 2 x))))"), Equal("(* -2 (sin (* 2 x)))")),
			"Expected (* 2 (* -1 (sin (* 2 x)))) or (* -2 (sin (* 2 x)))")

		test("(sin (+ x 1))", "(cos (+ x 1))", "sin(x+1) should return cos(x+1)")
		test("(sin (* 2 x))", "(* 2 (cos (* 2 x)))", "sin(2*x) should return 2*cos(2*x)")
		test("(tan (* 2 x))", "(* 2 (+ 1 (^ (tan (* 2 x)) 2)))", "tan(2*x) should return 2 * (1 + tan(2*x)^2)")
		test("(exp (* 2 x))", "(* 2 (exp (* 2 x)))", "exp(2*x) should return 2*exp(2*x)")
	})

	It("should work with second derivatives", func() {
		Expect(Diff(Diff("(sin x)"))).To(Equal("(* -1 (sin x))"), "Second deriv. sin(x) should return -1 * sin(x)")
		Expect(Diff(Diff("(exp x)"))).To(Equal("(exp x)"), "Second deriv. exp(x) should return exp(x)")

		// Accepting (* 3 (* 2 x)) or (* 6 x)
		Expect(Diff(Diff("(^ x 3)"))).To(Or(Equal("(* 3 (* 2 x))"), Equal("(* 6 x)")),
			"Expected (* 3 (* 2 x)) or (* 6 x)")
	})
})
