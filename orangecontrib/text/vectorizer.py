from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from Orange.data import Table, ContinuousVariable, Domain
from orangecontrib.text.utils import BaseWrapper, StringOption, FloatOption, BoolOption


class BaseVectorizerWrapper(BaseWrapper):
    name = "Vectorizer"
    vectorizer_cls = None
    preprocessor = None

    def update_configuration(self):
        kwargs = {opt.name: getattr(self, opt.name) for opt in self.options}
        self.vectorizer = self.vectorizer_cls(tokenizer=self.preprocessor, **kwargs)

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
    vectorizer_cls = CountVectorizer

    options = (
        FloatOption(name='min_df', default=0., verbose_name="Minimum term's document frequency."),
        FloatOption(name='max_df', default=1., verbose_name="Maximum term's document frequency."),
        BoolOption(name='binary', default=False, verbose_name="Binary"),
    )


class TfidfVectorizerWrapper(BaseVectorizerWrapper):
    name = "Tfidf vectorizer"
    vectorizer_cls = TfidfVectorizer

    NORMS = (
        ('No normalization', None),
        ('l1 normalization', 'l1'),
        ('l2 normalization', 'l2')
    )

    options = (
        FloatOption(name='min_df', default=0., verbose_name="Minimum terms document frequency."),
        FloatOption(name='max_df', default=1., verbose_name="Maximum terms document frequency."),
        BoolOption(name='binary', default=False, verbose_name="Binary"),
        StringOption(name='norm', default=None, verbose_name='Normalization method', choices=NORMS),
        BoolOption(name='use_idf', default=True, verbose_name='Enable idf reweighting'),
        BoolOption(name='smooth_idf', default=True, verbose_name='Smooth idf weights'),
        BoolOption(name='sublinear_tf', default=False, verbose_name='Apply sublinear tf scaling'),
    )
