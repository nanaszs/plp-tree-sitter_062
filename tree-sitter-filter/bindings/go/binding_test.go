package tree_sitter_filter_test

import (
	"testing"

	tree_sitter "github.com/tree-sitter/go-tree-sitter"
	tree_sitter_filter "github.com/tree-sitter/tree-sitter-filter/bindings/go"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_filter.Language())
	if language == nil {
		t.Errorf("Error loading Filter grammar")
	}
}
