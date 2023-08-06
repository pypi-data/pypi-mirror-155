from logging import getLogger

from opentelemetry.trace import Span

from helios.instrumentation.base_http_instrumentor import HeliosBaseHttpInstrumentor

_LOG = getLogger(__name__)


class HeliosRequestsInstrumentor(HeliosBaseHttpInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.requests'
    INSTRUMENTOR_NAME = 'RequestsInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None):
        if self.get_instrumentor() is None:
            return

        excluded_urls = ','.join(self.ignored_hostnames)
        self.get_instrumentor().instrument(tracer_provider=tracer_provider, span_callback=self.span_callback,
                                           excluded_urls=excluded_urls)

    @staticmethod
    def span_callback(span: Span, result) -> None:
        # result is an object of type requests.Response
        if result is None:
            return

        try:
            request = result.request
            if request is not None:
                HeliosRequestsInstrumentor.base_request_hook(span, request.headers, request.body)
        except Exception as error:
            _LOG.debug('requests request instrumentation error: %s.', error)

        try:
            response = result.raw
            if response is not None:
                HeliosRequestsInstrumentor.base_response_hook(span, response.headers, result._content)
        except Exception as error:
            _LOG.debug('requests response instrumentation error: %s.', error)
