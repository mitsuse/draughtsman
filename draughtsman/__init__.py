from cffi import FFI
from refract.json import LegacyJSONDeserialiser
from refract.contrib.apielements import registry, ParseResult


_all_ = ('parse',)


ffi = FFI()
ffi.cdef('''
typedef enum {
    DRAFTER_SERIALIZE_YAML = 0,
    DRAFTER_SERIALIZE_JSON
} drafter_format;

typedef struct {
    bool requireBlueprintName;
} drafter_parse_options;

typedef struct {
    bool sourcemap;
    drafter_format format;
} drafter_serialize_options;

int drafter_parse_blueprint_to(const char* source,
                               char** out,
                               const drafter_parse_options parse_opts,
                               const drafter_serialize_options serialize_opts);
''')

drafter = ffi.dlopen('drafter')


def parse(blueprint: str) -> ParseResult:
    source = ffi.new('char []', blueprint.encode('utf-8'))
    output = ffi.new('char **')
    serialize_options = ffi.new("drafter_serialize_options *", [False, 1])
    parse_options = ffi.new("drafter_parse_options *", [False])
    result = drafter.drafter_parse_blueprint_to(source, output, parse_options[0], serialize_options[0])

    if result != 0:
        raise Exception('Unknown Error')

    string = ffi.string(output[0]).decode('utf-8')
    deserialiser = LegacyJSONDeserialiser(registry=registry)
    return deserialiser.deserialise(string)
