from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from Orange.data import Table, ContinuousVariable, Domain
from orangecontrib.text.utils import BaseWrapper, StringOption, FloatOption, BoolOption, RangeOption


class BaseVectorizerWrapper(BaseWrapper):
    name = "Vectorizer"
    preprocessor = None

    options = (
        RangeOption(name='range', default=(0., 1.), verbose_name='Tf range'),
        BoolOption(name='binary', default=False, verbose_name="Binary"),
    )

    @property
    def vectorizer(self):
        return self.wrapped_object

    def apply_changes(self):
        kwargs = {opt.name: getattr(self, opt.name) for opt in self.options}
        min_df, max_df = kwargs.pop('range', None)
        kwargs['min_df'] = min_df
        kwargs['max_df'] = max_df
        self.wrapped_object = self.wrapped_class(tokenizer=self.preprocessor, **kwargs)

    def __call__(self, corpus):
        return self.fit_transform(corpus)

    def fit_transform(self, corpus):
        documents = corpus.documents
        feats = self.vectorizer.fit(documents)  # Features.
        freqs = feats.transform(documents).toarray()  # Frequencies.

        # Generate the domain attributes.
        attr = [ContinuousVariable(f) for f in feats.get_feature_names()]

        # Construct a new domain.
        domain = Domain(attr, corpus.domain.class_vars, metas=corpus.domain.metas)

        # Create the table.
        return Table.from_numpy(domain, freqs, Y=corpus._Y, metas=corpus.metas)


class CountVectorizerWrapper(BaseVectorizerWrapper):
    name = "Count vectorizer"
    wrapped_class = CountVectorizer


class TfidfVectorizerWrapper(BaseVectorizerWrapper):
    name = "Tfidf vectorizer"
    wrapped_class = TfidfVectorizer

    NORMS = (
        ('No normalization', None),
        ('l1 normalization', 'l1'),
        ('l2 normalization', 'l2')
    )

    options = BaseVectorizerWrapper.options + (
        StringOption(name='norm', default=None, verbose_name='Normalization method', choices=NORMS),
        BoolOption(name='use_idf', default=True, verbose_name='Enable idf reweighting'),
        BoolOption(name='smooth_idf', default=True, verbose_name='Smooth idf weights'),
        BoolOption(name='sublinear_tf', default=False, verbose_name='Apply sublinear tf scaling'),
    )
