import XCTest
import SwiftTreeSitter
import TreeSitterFilter

final class TreeSitterFilterTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_filter())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Filter grammar")
    }
}
