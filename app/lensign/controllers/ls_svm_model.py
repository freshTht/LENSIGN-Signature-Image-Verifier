from sklearn_crfsuite import CRF
def get_score(x):
  active_learning_crf.tagger_.set(x)
  return active_learning_crf.tagger_.probability(active_learning_crf.predict_single(x))

active_learning_crf = CRF(
  algorithm='lbfgs',
  c1=0.1,
  c2=0.1,
  max_iterations=100,
  all_possible_transitions=False
)