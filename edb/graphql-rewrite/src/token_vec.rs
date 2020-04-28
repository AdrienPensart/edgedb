use edb_graphql_parser::tokenizer::Token;
use edb_graphql_parser::position::Pos;


pub struct TokenVec<'a> {
    tokens: &'a Vec<(Token<'a>, Pos)>,
    consumed: usize,
}


impl<'a> TokenVec<'a> {
    pub fn new(tokens: &'a Vec<(Token<'a>, Pos)>) -> TokenVec {
        TokenVec {
            tokens,
            consumed: 0,
        }
    }
    pub fn drain<'x>(&'x mut self, n: usize)
        -> impl Iterator<Item=&(Token, Pos)> + 'x
    {
        let pos = self.consumed;
        self.consumed += n;
        assert!(n <= self.tokens.len(), "attempt to more tokens than exist");
        self.tokens[pos..][..n].iter()
    }
    pub fn drain_to<'x>(&'x mut self, end: usize)
        -> impl Iterator<Item=&(Token, Pos)> + 'x
    {
        let n = end.checked_sub(self.consumed)
            .expect("drain_to with index smaller than current");
        self.drain(n)
    }
    pub fn len(&self) -> usize {
        self.tokens.len().checked_sub(self.consumed)
            .expect("consumed more tokens than exists")
    }
}
