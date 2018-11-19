package kata_test

import (
	"testing"

	kata "github.com/dayfine/kata/coding-challenges/codewars/symbolic-diff-prefix-expr"
)

type test struct {
	input string
	want  string
	desc  string
}

func TestBasic(t *testing.T) {
	tests := []*test{
		{"5", "0", "constant should return 0"},
		{"x", "1", "x should return 1"},
		{"(+ x x)", "2", "x+x should return 2"},
		{"(- x x)", "0", "x-x should return 0"},
		{"(* x 2)", "2", "2*x should return 2"},
		{"(/ x 2)", "0.5", "x/2 should return 0.5"},
		{"(^ x 2)", "(* 2 x)", "x^2 should return 2*x"},
		{"(cos x)", "(* -1 (sin x))", "cos(x) should return -1 * sin(x)"},
		{"(sin x)", "(cos x)", "sin(x) should return cos(x)"},
		{"(tan x)", "(+ 1 (^ (tan x) 2))", "tan(x) should return 1 + tan(x)^2"},
		{"(exp x)", "(exp x)", "exp(x) should return exp(x)"},
		{"(ln x)", "(/ 1 x)", "ln(x) should return 1/x"},
	}

	for _, test := range tests {
		if got := kata.Diff(test.input); got != test.want {
			t.Errorf("Diff(%v) = %v, want: %v. %s.", test.input, got, test.want, test.desc)
		}
	}
}

func TestNested(t *testing.T) {
	tests := []*test{
		{"(+ x (+ x x))", "3", "x+(x+x) should return 3"},
		{"(- (+ x x) x)", "1", "(x+x)-x should return 1"},
		{"(* 2 (+ x 2))", "2", "2*(x+2) should return 2"},
		{"(/ 2 (+ 1 x))", "(/ -2 (^ (+ 1 x) 2))", "2/(1+x) should return -2/(1+x)^2"},
		{"(cos (+ x 1))", "(* -1 (sin (+ x 1)))", "cos(x+1) should return -1 * sin(x+1)"},
		{"(sin (+ x 1))", "(cos (+ x 1))", "sin(x+1) should return cos(x+1)"},
		{"(sin (* 2 x))", "(* 2 (cos (* 2 x)))", "sin(2*x) should return 2*cos(2*x)"},
		{"(tan (* 2 x))", "(* 2 (+ 1 (^ (tan (* 2 x)) 2)))", "tan(2*x) should return 2 * (1 + tan(2*x)^2)"},
		{"(exp (* 2 x))", "(* 2 (exp (* 2 x)))", "exp(2*x) should return 2*exp(2*x)"},
		// Accepting (* 2 (* -1 (sin (* 2 x)))) or (* -2 (sin (* 2 x)))
		// Expect(Diff("(cos (* 2 x))")).To(Or(Equal("(* 2 (* -1 (sin (* 2 x))))"), Equal("(* -2 (sin (* 2 x)))")),
		//	"Expected (* 2 (* -1 (sin (* 2 x)))) or (* -2 (sin (* 2 x)))")
	}

	for _, test := range tests {
		if got := kata.Diff(test.input); got != test.want {
			t.Errorf("Diff(%v) = %v, want: %v. %s.", test.input, got, test.want, test.desc)
		}
	}
}

func TestSecondDerv(t *testing.T) {
	tests := []*test{
		{"(sin x)", "(* -1 (sin x))", "Second deriv. sin(x) should return -1 * sin(x)"},
		{"(exp x)", "(exp x)", "Second deriv. exp(x) should return exp(x)"},
		// Accepting (* 3 (* 2 x)) or (* 6 x)
		//Expect(Diff(Diff("(^ x 3)"))).To(Or(Equal("(* 3 (* 2 x))"), Equal("(* 6 x)")),
		//	"Expected (* 3 (* 2 x)) or (* 6 x)")
	}

	for _, test := range tests {
		if got := kata.Diff(kata.Diff(test.input)); got != test.want {
			t.Errorf("Diff(Diff(%v)) = %v, want: %v. %s.", test.input, got, test.want, test.desc)
		}
	}
}
