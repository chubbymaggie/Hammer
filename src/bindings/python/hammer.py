from cffi import FFI
import threading
import sys

_ffi = FFI()

# {{{ Types

_ffi.cdef("typedef struct HAllocator_ HAllocator;")
_ffi.cdef("typedef struct HArena_ HArena;")
_ffi.cdef("typedef int bool;")
_ffi.cdef("typedef struct HParseState_ HParseState;")
_ffi.cdef("""
typedef enum HParserBackend_ {
  PB_MIN = 0,
  PB_PACKRAT = 0, // PB_MIN is always the default.
  PB_REGULAR,
  PB_LLk,
  PB_LALR,
  PB_GLR
// TODO: support PB_MAX
} HParserBackend;
""")
_ffi.cdef("""
typedef enum HTokenType_ {
  // Before you change the explicit values of these, think of the poor bindings ;_;
  TT_NONE = 1,
  TT_BYTES = 2,
  TT_SINT = 4,
  TT_UINT = 8,
  TT_SEQUENCE = 16,
  TT_RESERVED_1, // reserved for backend-specific internal use
  TT_ERR = 32,
  TT_USER = 64,
  TT_MAX
} HTokenType;
""")
_ffi.cdef("""
typedef struct HCountedArray_ {
  size_t capacity;
  size_t used;
  HArena * arena;
  struct HParsedToken_ **elements;
} HCountedArray;
""")
_ffi.cdef("""
typedef struct HBytes_ {
  const uint8_t *token;
  size_t len;
} HBytes;
""")
_ffi.cdef("""
typedef struct HParsedToken_ {
  HTokenType token_type;
  union {
    HBytes bytes;
    int64_t sint;
    uint64_t uint;
    double dbl;
    float flt;
    HCountedArray *seq; // a sequence of HParsedToken's
    void *user;
  };
  size_t index;
  char bit_offset;
} HParsedToken;
""")
_ffi.cdef("""
typedef struct HParseResult_ {
  const HParsedToken *ast;
  long long bit_length;
  HArena * arena;
} HParseResult;
""")

_ffi.cdef("""typedef HParsedToken* (*HAction)(const HParseResult *p);""")
_ffi.cdef("""typedef bool (*HPredicate)(HParseResult *p);""")
_ffi.cdef("""
typedef struct HCFChoice_ HCFChoice;
typedef struct HRVMProg_ HRVMProg;
typedef struct HParserVtable_ HParserVtable;
""")

_ffi.cdef("typedef struct HParser_ HParser;")
_ffi.cdef("""
typedef struct HParserTestcase_ {
  unsigned char* input;
  size_t length;
  char* output_unambiguous;
} HParserTestcase;

typedef struct HCaseResult_ {
  bool success;
  union {
    const char* actual_results; // on failure, filled in with the results of h_write_result_unamb
    size_t parse_time; // on success, filled in with time for a single parse, in nsec
  };
} HCaseResult;

typedef struct HBackendResults_ {
  HParserBackend backend;
  bool compile_success;
  size_t n_testcases;
  size_t failed_testcases; // actually a count...
  HCaseResult *cases;
} HBackendResults;

typedef struct HBenchmarkResults_ {
  size_t len;
  HBackendResults *results;
} HBenchmarkResults;
""")

# }}}
# {{{ Arena functions
_ffi.cdef("void* h_arena_malloc(HArena *arena, size_t count);")
_ffi.cdef("void h_arena_free(HArena *arena, void* ptr);")
# }}}
# {{{ cdefs
## The following section was generated by
## $ perl ../desugar-header.pl <../../hammer.h |sed -e 's/.*/_ffi.cdef("&")/'
_ffi.cdef("HParseResult* h_parse(const HParser* parser, const uint8_t* input, size_t length);")
_ffi.cdef("HParseResult* h_parse__m(HAllocator* mm__, const HParser* parser, const uint8_t* input, size_t length);")
_ffi.cdef("HParser* h_token(const uint8_t *str, const size_t len);")
_ffi.cdef("HParser* h_token__m(HAllocator* mm__, const uint8_t *str, const size_t len);")
_ffi.cdef("HParser* h_ch(const uint8_t c);")
_ffi.cdef("HParser* h_ch__m(HAllocator* mm__, const uint8_t c);")
_ffi.cdef("HParser* h_ch_range(const uint8_t lower, const uint8_t upper);")
_ffi.cdef("HParser* h_ch_range__m(HAllocator* mm__, const uint8_t lower, const uint8_t upper);")
_ffi.cdef("HParser* h_int_range(const HParser *p, const int64_t lower, const int64_t upper);")
_ffi.cdef("HParser* h_int_range__m(HAllocator* mm__, const HParser *p, const int64_t lower, const int64_t upper);")
_ffi.cdef("HParser* h_bits(size_t len, bool sign);")
_ffi.cdef("HParser* h_bits__m(HAllocator* mm__, size_t len, bool sign);")
_ffi.cdef("HParser* h_int64(void);")
_ffi.cdef("HParser* h_int64__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_int32(void);")
_ffi.cdef("HParser* h_int32__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_int16(void);")
_ffi.cdef("HParser* h_int16__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_int8(void);")
_ffi.cdef("HParser* h_int8__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_uint64(void);")
_ffi.cdef("HParser* h_uint64__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_uint32(void);")
_ffi.cdef("HParser* h_uint32__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_uint16(void);")
_ffi.cdef("HParser* h_uint16__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_uint8(void);")
_ffi.cdef("HParser* h_uint8__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_whitespace(const HParser* p);")
_ffi.cdef("HParser* h_whitespace__m(HAllocator* mm__, const HParser* p);")
_ffi.cdef("HParser* h_left(const HParser* p, const HParser* q);")
_ffi.cdef("HParser* h_left__m(HAllocator* mm__, const HParser* p, const HParser* q);")
_ffi.cdef("HParser* h_right(const HParser* p, const HParser* q);")
_ffi.cdef("HParser* h_right__m(HAllocator* mm__, const HParser* p, const HParser* q);")
_ffi.cdef("HParser* h_middle(const HParser* p, const HParser* x, const HParser* q);")
_ffi.cdef("HParser* h_middle__m(HAllocator* mm__, const HParser* p, const HParser* x, const HParser* q);")
_ffi.cdef("HParser* h_action(const HParser* p, const HAction a);")
_ffi.cdef("HParser* h_action__m(HAllocator* mm__, const HParser* p, const HAction a);")
_ffi.cdef("HParser* h_in(const uint8_t *charset, size_t length);")
_ffi.cdef("HParser* h_in__m(HAllocator* mm__, const uint8_t *charset, size_t length);")
_ffi.cdef("HParser* h_not_in(const uint8_t *charset, size_t length);")
_ffi.cdef("HParser* h_not_in__m(HAllocator* mm__, const uint8_t *charset, size_t length);")
_ffi.cdef("HParser* h_end_p(void);")
_ffi.cdef("HParser* h_end_p__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_nothing_p(void);")
_ffi.cdef("HParser* h_nothing_p__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_sequence(HParser* p, ...);")
_ffi.cdef("HParser* h_sequence__m(HAllocator *mm__, HParser* p, ...);")
_ffi.cdef("HParser* h_sequence__a(void* args);")
_ffi.cdef("HParser* h_sequence__ma(HAllocator* mm__, void* args);")
_ffi.cdef("HParser* h_choice(HParser* p, ...);")
_ffi.cdef("HParser* h_choice__m(HAllocator *mm__, HParser* p, ...);")
_ffi.cdef("HParser* h_choice__a(void* args);")
_ffi.cdef("HParser* h_choice__ma(HAllocator* mm__, void* args);")
_ffi.cdef("HParser* h_butnot(const HParser* p1, const HParser* p2);")
_ffi.cdef("HParser* h_butnot__m(HAllocator* mm__, const HParser* p1, const HParser* p2);")
_ffi.cdef("HParser* h_difference(const HParser* p1, const HParser* p2);")
_ffi.cdef("HParser* h_difference__m(HAllocator* mm__, const HParser* p1, const HParser* p2);")
_ffi.cdef("HParser* h_xor(const HParser* p1, const HParser* p2);")
_ffi.cdef("HParser* h_xor__m(HAllocator* mm__, const HParser* p1, const HParser* p2);")
_ffi.cdef("HParser* h_many(const HParser* p);")
_ffi.cdef("HParser* h_many__m(HAllocator* mm__, const HParser* p);")
_ffi.cdef("HParser* h_many1(const HParser* p);")
_ffi.cdef("HParser* h_many1__m(HAllocator* mm__, const HParser* p);")
_ffi.cdef("HParser* h_repeat_n(const HParser* p, const size_t n);")
_ffi.cdef("HParser* h_repeat_n__m(HAllocator* mm__, const HParser* p, const size_t n);")
_ffi.cdef("HParser* h_optional(const HParser* p);")
_ffi.cdef("HParser* h_optional__m(HAllocator* mm__, const HParser* p);")
_ffi.cdef("HParser* h_ignore(const HParser* p);")
_ffi.cdef("HParser* h_ignore__m(HAllocator* mm__, const HParser* p);")
_ffi.cdef("HParser* h_sepBy(const HParser* p, const HParser* sep);")
_ffi.cdef("HParser* h_sepBy__m(HAllocator* mm__, const HParser* p, const HParser* sep);")
_ffi.cdef("HParser* h_sepBy1(const HParser* p, const HParser* sep);")
_ffi.cdef("HParser* h_sepBy1__m(HAllocator* mm__, const HParser* p, const HParser* sep);")
_ffi.cdef("HParser* h_epsilon_p(void);")
_ffi.cdef("HParser* h_epsilon_p__m(HAllocator* mm__);")
_ffi.cdef("HParser* h_length_value(const HParser* length, const HParser* value);")
_ffi.cdef("HParser* h_length_value__m(HAllocator* mm__, const HParser* length, const HParser* value);")
_ffi.cdef("HParser* h_attr_bool(const HParser* p, HPredicate pred);")
_ffi.cdef("HParser* h_attr_bool__m(HAllocator* mm__, const HParser* p, HPredicate pred);")
_ffi.cdef("HParser* h_and(const HParser* p);")
_ffi.cdef("HParser* h_and__m(HAllocator* mm__, const HParser* p);")
_ffi.cdef("HParser* h_not(const HParser* p);")
_ffi.cdef("HParser* h_not__m(HAllocator* mm__, const HParser* p);")
_ffi.cdef("HParser* h_indirect(void);")
_ffi.cdef("HParser* h_indirect__m(HAllocator* mm__);")
_ffi.cdef("void h_bind_indirect(HParser* indirect, const HParser* inner);")
_ffi.cdef("void h_bind_indirect__m(HAllocator* mm__, HParser* indirect, const HParser* inner);")
_ffi.cdef("void h_parse_result_free(HParseResult *result);")
_ffi.cdef("void h_parse_result_free__m(HAllocator* mm__, HParseResult *result);")
_ffi.cdef("void h_pprint(FILE* stream, const HParsedToken* tok, int indent, int delta);")
_ffi.cdef("int h_compile(HParser* parser, HParserBackend backend, const void* params);")
_ffi.cdef("int h_compile__m(HAllocator* mm__, HParser* parser, HParserBackend backend, const void* params);")
_ffi.cdef("HBenchmarkResults * h_benchmark(HParser* parser, HParserTestcase* testcases);")
_ffi.cdef("HBenchmarkResults * h_benchmark__m(HAllocator* mm__, HParser* parser, HParserTestcase* testcases);")

_lib = _ffi.verify("#include <hammer/hammer.h>",
                 libraries=['hammer'])

_lib.TT_PYTHON = _lib.TT_USER # TODO: Use the token type allocator from #45
# }}}
class _DynamicScopeHolder(threading.local):
    """A dynamically-scoped holder of python objects, which may or may not
    otherwise appear in the object graph. Intended for use with CFFI """
    def __init__(self):
        self._ctxstack = []
    def __enter__(self):
        self._ctxstack.append([])
    def __exit__(self, exc_type, exc_value, traceback):
        self._ctxstack.pop()
        return False
    def stash(self, *objs):
        if len(self._ctxstack) < 1:
            raise Exception("Not in any dynamic scope")
        for obj in objs:
            self._ctxstack[-1].append(obj)
def _fromHParsedToken(cobj):
    # TODO: Free the toplevel parser
    tt = cobj.token_type

    if cobj.token_type == _lib.TT_BYTES:
        return _ffi.buffer(cobj.bytes.token, cobj.bytes.len)[:]
    elif cobj.token_type == _lib.TT_ERR:
        # I have no idea what this is for
        pass
    elif cobj.token_type == _lib.TT_NONE:
        return None
    elif cobj.token_type == _lib.TT_SEQUENCE:
        return [_fromHParsedToken(cobj.seq.elements[i])
                for i in range(cobj.seq.used)]
    elif cobj.token_type == _lib.TT_SINT:
        return cobj.sint
    elif cobj.token_type == _lib.TT_UINT:
        return cobj.uint
    elif cobj.token_type == _lib.TT_PYTHON:
        return _ffi.from_handle(cobj.user)

_parser_result_holder = _DynamicScopeHolder()
def _toHParsedToken(arena, pyobj):
    if pyobj is None:
        return _ffi.NULL
    cobj = _ffi.new_handle(pyobj)
    _parser_result_holder.stash(cobj)

    hpt = _ffi.cast("HParsedToken*", _lib.h_arena_malloc(arena, _ffi.sizeof("HParsedToken")))
    hpt.token_type = _lib.TT_PYTHON
    hpt.user = cobj
    hpt.bit_offset = chr(127)
    hpt.index = 0
    return hpt

def _fromParseResult(cobj):
    ret = _fromHParsedToken(cobj.ast)
    _lib.h_parse_result_free(cobj)
    return ret

def _to_haction(fn):
    """Turn a function that transforms a parsed value into an HAction"""
    def action(parse_result):
        res = _toHParsedToken(parse_result.arena,  fn(_fromParseResult(parse_result)))
        if res != _ffi.NULL and parse_result.ast != _ffi.NULL:
            res.index = parse_result.ast.index
            res.bit_offset = parse_result.ast.bit_offset
        return res
    return _ffi.callback("HParsedToken*(HParseResult*)", action)

def _to_hpredicate(fn):
    """Turn a function that transforms a parsed value into an HAction"""
    def predicate(parse_result):
        res = fn(_fromParseResult(parse_result))
        # TODO: Handle exceptions; parse should fail.
        if type(res) != bool:
            raise TypeError("Predicates should return a bool")
        return res
    return _ffi.callback("bool(HParseResult*)", predicate)

class Parser(object):
    # TODO: Map these to individually garbage-collected blocks of
    # memory. Perhaps with an arena allocator with block size of 1?
    # There has to be something more efficient than that, though.

    # TODO: How do we handle encodings? By default, we're using UTF-8
    def __init__(self, internal, deps):
        """Create a new parser from an FFI object. Not for user code"""
        self._parser = internal
        self._deps = deps

    def parse(self, string):
        with _parser_result_holder:
            pres = _lib.h_parse(self._parser, string, len(string))
            if pres:
                return _fromParseResult(pres)
            else:
                return None

    def __mul__(self, count):
        return repeat_n(self, count)


                
class IndirectParser(Parser):
    def bind(self, inner):
        _lib.h_bind_indirect(self._parser, inner._parser)
        self._deps = (inner,)

class BitsParser(Parser):
    pass

def token(token):
    # TODO: Does not clone argument.
    if isinstance(token, unicode):
        token = token.encode("utf-8")
    return Parser(_lib.h_token(token, len(token)), ())

def ch(char):
    """Returns either a token or an int, depending on the type of the
    argument"""
    if isinstance(char, int):
        return Parser(_lib.h_ch(char), ())
    else:
        return token(char)

def ch_range(chr1, chr2):
    if not isinstance(chr1, str) or not isinstance(chr2, str):
        raise TypeError("ch_range can't handle unicode")
    def my_action(pr):
        # print "In action: ", pr
        return pr
    return action(Parser(_lib.h_ch_range(ord(chr1), ord(chr2)), ()), my_action)

def int_range(parser, i1, i2):
    if type(parser) != BitsParser:
        raise TypeError("int_range is only valid when used with a bits parser")
    return Parser(_lib.h_int_range(parser._parser, i1, i2), (parser,))

def bits(length, signedp):
    return BitsParser(_lib.h_bits(length, signedp), ())

def int64(): return bits(64, True)
def int32(): return bits(32, True)
def int16(): return bits(16, True)
def int8 (): return bits(8,  True)
def uint64(): return bits(64, False)
def uint32(): return bits(32, False)
def uint16(): return bits(16, False)
def uint8 (): return bits(8,  False)

def whitespace(p):
    return Parser(_lib.h_whitespace(p._parser), (p,))
def left(p1, p2):
    return Parser(_lib.h_left(p1._parser, p2._parser), (p1, p2))
def right(p1, p2):
    return Parser(_lib.h_right(p1._parser, p2._parser), (p1, p2))
def middle(p1, p2, p3):
    return Parser(_lib.h_middle(p1._parser, p2._parser, p3._parser), (p1, p2, p3))
def action(parser, action):
    caction = _to_haction(action)
    return Parser(_lib.h_action(parser._parser, caction), (parser, caction))

def in_(charset):
    if not isinstance(charset, str):
        # TODO/Python3: change str to bytes
        raise TypeError("in_ can't deal with unicode")
    return Parser(_lib.h_in(charset, len(charset)), ())
def not_in(charset):
    if not isinstance(charset, str):
        # TODO/Python3: change str to bytes
        raise TypeError("in_ can't deal with unicode")
    return Parser(_lib.h_not_in(charset, len(charset)), ())
def end_p():
    return Parser(_lib.h_end_p(), ())
def nothing_p():
    return Parser(_lib.h_nothing_p(), ())
def sequence(*parsers):
    plist = [p._parser for p in parsers]
    plist.append(_ffi.NULL)
    return Parser(_lib.h_sequence(*plist), (plist,))
def choice(*parsers):
    plist = [p._parser for p in parsers]
    plist.append(_ffi.NULL)
    return Parser(_lib.h_choice(*plist), (plist,))
def butnot(p1, p2):
    return Parser(_lib.h_butnot(p1._parser, p2._parser), (p1, p2))
def difference(p1, p2):
    return Parser(_lib.h_difference(p1._parser, p2._parser), (p1, p2))
def xor(p1, p2):
    return Parser(_lib.h_xor(p1._parser, p2._parser), (p1, p2))
def many(p1):
    return Parser(_lib.h_many(p1._parser), (p1,))
def many1(p1):
    return Parser(_lib.h_many1(p1._parser), (p1,))
def repeat_n(p1, n):
    return Parser(_lib.h_repeat_n(p1._parser, n), (p1,))
def optional(p1):
    return Parser(_lib.h_optional(p1._parser), (p1,))
def ignore(p1):
    return Parser(_lib.h_ignore(p1._parser), (p1,))
def sepBy(p, sep):
    return Parser(_lib.h_sepBy(p._parser, sep._parser), (p, sep))
def sepBy1(p, sep):
    return Parser(_lib.h_sepBy1(p._parser, sep._parser), (p, sep))
def epsilon_p():
    return Parser(_lib.h_epsilon_p(), ())
def length_value(p_len, p_value):
    return Parser(_lib.h_length_value(p_len._parser, p_value._parser), (p_len, p_value))
def attr_bool(parser, predicate):
    cpredicate = _to_hpredicate(predicate)
    return Parser(_lib.h_attr_bool(parser._parser, cpredicate), (parser, cpredicate))
def and_(parser):
    return Parser(_lib.h_and(parser._parser), (parser,))
def not_(parser):
    return Parser(_lib.h_not(parser._parser), (parser,))
def indirect():
    return IndirectParser(_lib.h_indirect(), ())
def bind_indirect(indirect, inner):
    indirect.bind(inner)

def parse(parser):
    return parser.parse()

# Unfortunately, "in", "and", and "not" are keywords. This makes them
# show up in the module namespace for the use of automated tools. Do
# not attempt to use them by hand; only use the mangled forms (with
# the '_')
sys.modules[__name__].__dict__["in"] = in_
sys.modules[__name__].__dict__["and"] = and_
sys.modules[__name__].__dict__["not"] = not_

def run_test():
    p_test = sepBy1(choice(ch('1'),
                           ch('2'),
                           ch('3')),
                    ch(','))
    return p_test.parse("1,2,3")

# {{{ Automatic parser construction... python specific

# TODO: Implement Parsable metaclass, which requires the existence of
# a "parse" method.

# This is expected to be extended by user code. As a general rule,
# only provide auto-parsers for your own types.
AUTO_PARSERS = {
    str: token,
    unicode: token,
}

def _auto_seq(lst):
    return sequence(*(auto_1(p, default_method=_auto_choice)
                      for p in lst))
        
def _auto_choice(lst):
    return choice(*(auto_1(p, default_method=_auto_seq)
                    for p in lst))

def auto_1(arg, default_method=_auto_choice):
    if isinstance(arg, Parser):
        return arg
    elif type(arg) in AUTO_PARSERS:
        return AUTO_PARSERS[type(arg)](arg)
    else:
        return default_method(arg)

def auto(*args):
    return auto_1(args, default_method=_auto_choice)

# }}}