from pytest_bdd import scenarios, given, when, then, parsers

# Scenarios
from edam.reader.resolvers.resolver_factory import ResolverFactory

scenarios('../features/read_csv.feature')


# Given Steps

@given(parsers.parse('EDAM starts with "{input_file}","{metadata_file}" '
                     'and "{template_file}"'), target_fixture='factory')
def step_impl(input_file, metadata_file, template_file):
    factory = ResolverFactory(input_uri=input_file,
                              template=template_file,
                              metadata_file=metadata_file)
    return factory


@when("the user attempts to import data", target_fixture="resolver")
def step_impl(factory):
    return factory.resolver


@then(parsers.parse('output contains "{timeseries_length}" timeseries'))
def step_impl(timeseries_length, resolver):
    assert len(resolver.timeseries) == int(timeseries_length)
