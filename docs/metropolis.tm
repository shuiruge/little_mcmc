<TeXmacs|1.99.1>

<style|generic>

<\body>
  <\hide-preamble>
    \;

    <assign||<macro|>>
  </hide-preamble>

  This documentation provides an illustration (and also a proof) of
  Metropolis-Hastings algorithm of sampling. The proof follows Metropolis et
  al (1953), but is modified and generalized in its morden face.

  <\notation>
    [Discrete Version]<\footnote>
      [Continuum Version] Let <math|<with|math-font|cal|X>> state-space of a
      given stochastic system. Let <math|p<around*|(|x|)>> denotes the target
      distribution to be mimicked. Let <math|q<around*|(|x\<rightarrow\>y|)>>
      (or <math|q<around*|(|y\|x|)>> by statistics) the proposed
      transition-distribution of Markov process from state <math|x> to
      <math|y>. Suppose, for any <math|x,y\<in\><with|math-font|cal|X>>,
      <math|q<around*|(|x\<rightarrow\>y|)>\<neq\>0> and
      <math|p<around*|(|x|)>\<neq\>0> (thus they are positive). That is, in
      <math|<with|math-font|cal|X>> any <math|x> and <math|y> are
      ``connected''. And for Metropolis algorithm,
      <math|q<around*|(|x\<rightarrow\>y|)>=q<around*|(|y\<rightarrow\>x|)>>
      for <math|\<forall\>x,y\<in\><with|math-font|cal|X>> is supposed.
    </footnote> Let <math|<with|math-font|cal|X>> state-space of a given
    stochastic system. Suppose <math|<with|math-font|cal|X>> is discrete or
    has been discretized, within which state is denoted by <math|x<rsub|r>>,
    or simply <math|r>. Let <math|p<around*|(|r|)>> denotes the target
    distribution to be mimicked. Let <math|q<around*|(|r\<rightarrow\>s|)>>
    (or <math|q<around*|(|s\|r|)>> by statistics) the proposed
    transition-distribution of Markov process from state <math|r> to
    <math|s>. Suppose, for any <math|r,s\<in\><with|math-font|cal|X>>,
    <math|q<around*|(|r\<rightarrow\>s|)>\<neq\>0> and
    <math|p<around*|(|r|)>\<neq\>0> (thus they are positive). That is, in
    <math|<with|math-font|cal|X>> any <math|r> and <math|s> are
    ``connected''. And for Metropolis algorithm,
    <math|q<around*|(|r\<rightarrow\>s|)>=q<around*|(|s\<rightarrow\>r|)>>
    for <math|\<forall\>r,s\<in\><with|math-font|cal|X>> is supposed.
  </notation>

  <\algorithm>
    <label|algorithm: Metropolis>[Metropolis]

    #!/usr/bin/env python3

    # -*- coding: utf-8 -*-

    \;

    import random

    \;

    class MetropolisSampler:

    \ \ \ \ """

    \ \ \ \ Args:

    \ \ \ \ \ \ \ \ iterations: int

    \ \ \ \ \ \ \ \ initialize_state: (None -\<gtr\> State)

    \ \ \ \ \ \ \ \ markov_process: (State -\<gtr\> State)

    \ \ \ \ \ \ \ \ burn_in: int

    \;

    \ \ \ \ Attributes:

    \ \ \ \ \ \ \ \ accept_ratio: float

    \ \ \ \ \ \ \ \ \ \ \ \ Generated only after calling MetropolisSampler.

    \;

    \ \ \ \ Methods:

    \ \ \ \ \ \ \ \ sampling:

    \ \ \ \ \ \ \ \ \ \ \ \ Do the sampling by Metropolis algorithm.

    \;

    \ \ \ \ Remarks:

    \ \ \ \ \ \ \ \ The "State" can be any abstract class.

    \ \ \ \ """

    \;

    \;

    \ \ \ \ def __init__(self, iterations, initialize_state, markov_process,
    burn_in):

    \;

    \ \ \ \ \ \ \ \ self.iterations = iterations

    \ \ \ \ \ \ \ \ self.initialize_state = initialize_state

    \ \ \ \ \ \ \ \ self.markov_process = markov_process

    \ \ \ \ \ \ \ \ self.burn_in = burn_in

    \;

    \;

    \ \ \ \ def sampling(self, target_distribution):

    \ \ \ \ \ \ \ \ """

    \ \ \ \ \ \ \ \ Do the sampling.

    \;

    \ \ \ \ \ \ \ \ Args:

    \ \ \ \ \ \ \ \ \ \ \ \ target_distribution: (State -\<gtr\> float)

    \;

    \ \ \ \ \ \ \ \ Returns:

    \ \ \ \ \ \ \ \ \ \ \ \ list of State, with length being iterations -
    burn_in.

    \ \ \ \ \ \ \ \ """

    \;

    \ \ \ \ \ \ \ \ init_state = self.initialize_state()

    \ \ \ \ \ \ \ \ assert target_distribution(init_state) \<gtr\> 0

    \;

    \ \ \ \ \ \ \ \ chain = [init_state]

    \ \ \ \ \ \ \ \ accepted = 0

    \;

    \ \ \ \ \ \ \ \ for i in range(self.iterations):

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ next_state = self.markov_process(init_state)

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ alpha = target_distribution(next_state) /
    target_distribution(init_state)

    \ \ \ \ \ \ \ \ \ \ \ \ u = random.uniform(0, 1)

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ if alpha \<gtr\> u:

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ accepted += 1

    \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ chain.append(next_state)

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ init_state = next_state.copy()

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ else:

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ chain.append(init_state)

    \;

    \ \ \ \ \ \ \ \ self.accept_ratio = accepted / self.iterations

    \ \ \ \ \ \ \ \ print('accept-ratio = {0}'.format(self.accept_ratio))

    \;

    \ \ \ \ \ \ \ \ return chain[self.burn_in:]
  </algorithm>

  <\lemma>
    <label|lemma: transition>Define, for <math|\<forall\>r\<in\><with|math-font|cal|X>>,
    <math|J<around*|(|r|)>\<assign\><around*|{|\<forall\>s\<in\><with|math-font|cal|X>:
    p<around*|(|r|)>\<geqslant\>p<around*|(|s|)>|}>>. Let
    <math|h<rsub|i><around*|(|r|)>> the distribution of
    <math|\<forall\>r\<in\><with|math-font|cal|X>> at the <math|i>th Markov
    epoch. For any given <math|h<rsub|i>>, we have

    <\equation*>
      h<rsub|i+1><around*|(|r|)>-h<rsub|i><around*|(|r|)>=<big|sum><rsub|s\<in\><with|math-font|cal|X>><around*|{|q<around*|(|s\<rightarrow\>r|)><around*|[|
      <frac|\<delta\><rsub|s\<in\>J<around*|(|r|)>>|p<around*|(|r|)>>+<frac|\<delta\><rsub|s\<nin\>J<around*|(|r|)>>|p<around*|(|s|)>>|]>|}>
      <around*|{|h<rsub|i><around*|(|s|)>
      p<around*|(|r|)>-h<rsub|i><around*|(|r|)> p<around*|(|s|)>|}>.
    </equation*>

    Note that the first <math|<around*|{|\<ldots\>|}>> are symmetric for
    <math|s> and <math|r>, while the second is anti-symmtric.
  </lemma>

  <\proof>
    Directly from Metropolis algorithm, we have,

    <\eqnarray*>
      <tformat|<table|<row|<cell|h<rsub|i+1><around*|(|r|)>-h<rsub|i><around*|(|r|)>>|<cell|=>|<cell|<big|sum><rsub|s\<in\>J<around*|(|r|)>>
      h<rsub|i><around*|(|s|)> q<around*|(|s\<rightarrow\>r|)>+<big|sum><rsub|s\<nin\>J<around*|(|r|)>>
      h<rsub|i><around*|(|s|)> q<around*|(|s\<rightarrow\>r|)>
      <frac|p<around*|(|r|)>|p<around*|(|s|)>>>>|<row|<cell|>|<cell|->|<cell|<big|sum><rsub|s\<in\>J<around*|(|r|)>>
      h<rsub|i><around*|(|r|)> q<around*|(|r\<rightarrow\>s|)>
      <frac|p<around*|(|s|)>|p<around*|(|r|)>>+<big|sum><rsub|s\<nin\>J<around*|(|r|)>>
      h<rsub|i><around*|(|r|)> q<around*|(|r\<rightarrow\>s|)>.>>>>
    </eqnarray*>

    Since, in Metropolis algorithm, <math|q<around*|(|s\<rightarrow\>r|)>=q<around*|(|r\<rightarrow\>s|)>>
    is supposed,

    <\eqnarray*>
      <tformat|<table|<row|<cell|h<rsub|i+1><around*|(|r|)>-h<rsub|i><around*|(|r|)>>|<cell|=>|<cell|<big|sum><rsub|s\<in\>J<around*|(|r|)>>
      h<rsub|i><around*|(|s|)> q<around*|(|s\<rightarrow\>r|)>+<big|sum><rsub|s\<nin\>J<around*|(|r|)>>
      h<rsub|i><around*|(|s|)> q<around*|(|s\<rightarrow\>r|)>
      <frac|p<around*|(|r|)>|p<around*|(|s|)>>>>|<row|<cell|>|<cell|->|<cell|<big|sum><rsub|s\<in\>J<around*|(|r|)>>
      h<rsub|i><around*|(|r|)> q<around*|(|s\<rightarrow\>r|)>
      <frac|p<around*|(|s|)>|p<around*|(|r|)>>+<big|sum><rsub|s\<nin\>J<around*|(|r|)>>
      h<rsub|i><around*|(|r|)> q<around*|(|s\<rightarrow\>r|)>;>>>>
    </eqnarray*>

    then by direct simplification, we reach

    <\equation*>
      h<rsub|i+1><around*|(|r|)>-h<rsub|i><around*|(|r|)>=<big|sum><rsub|s\<in\><with|math-font|cal|X>><around*|{|q<around*|(|s\<rightarrow\>r|)><around*|[|
      <frac|\<delta\><rsub|s\<in\>J<around*|(|r|)>>|p<around*|(|r|)>>+<frac|\<delta\><rsub|s\<nin\>J<around*|(|r|)>>|p<around*|(|s|)>>|]>|}>
      <around*|{|h<rsub|i><around*|(|s|)>
      p<around*|(|r|)>-h<rsub|i><around*|(|r|)> p<around*|(|s|)>|}>.
    </equation*>
  </proof>

  <\corollary>
    <label|corollary: Existence of Stable Distribution>If <math|h<rsub|i>=p>,
    then <math|h<rsub|i+1>=p>.
  </corollary>

  <\theorem>
    <label|theorem: Metropolis>[Metropolis] Samples generated by algorithm
    <reference|algorithm: Metropolis> approximately obeys the target
    distribution <math|p<around*|(|x|)>>. That is, algorithm
    <reference|algorithm: Metropolis> creates a sampler of
    <math|p<around*|(|x|)>>.
  </theorem>

  <\proof>
    [Intuitive]

    Let <math|\<forall\>r<rsub|r>\<in\>\<cal-X\>> given. We have an infinite
    Markov chain generated by Metropolis algorithm starting at
    <math|r<rsub|1>>, say <math|<around*|{|r<rsub|1>,r<rsub|2>,\<ldots\>,r<rsub|N>|}>>.
    We want to prove that <math|<around*|{|r<rsub|1>,r<rsub|2>,\<ldots\>,r<rsub|N>|}>>
    obeys distribution <math|p<around*|(|x|)>>.

    Define <math|h> by <math|<around*|{|r<rsub|1>,r<rsub|2>,\<ldots\>,r<rsub|N-1>|}>\<sim\>h>.
    That is, the histogram of <math|<around*|{|r<rsub|0>,r<rsub|1>,\<ldots\>,r<rsub|N-1>|}>>,
    after normalization, can be fitted by <math|h>. Then,
    <math|<around*|{|r<rsub|1>,r<rsub|2>,\<ldots\>,r<rsub|N-1>|}>\<sim\>h>,
    since, if <math|N> is large, dropping <math|r<rsub|1>> affects little on
    the fitting of histogram. On the other side, we shall not forget that
    <math|<around*|{|r<rsub|1>,r<rsub|2>,\<ldots\>,r<rsub|N>|}>> are
    generated by a Markov chain asdf. Thus, the Metropolis algorithm as a
    Markov process brings <math|r<rsub|i>\<rightarrow\>r<rsub|i+1>> for
    <math|\<forall\>r=1,\<ldots\>,N-1>, s.t.
    <math|<around*|{|r<rsub|1>,r<rsub|2>,\<ldots\>,r<rsub|N-1>|}>\<rightarrow\><around*|{|r<rsub|2>,r<rsub|3>,\<ldots\>,r<rsub|N>|}>>.
    Let <math|h<rprime|'>> generated by Metropolis algorithm from <math|h>,
    that is, <math|h<rprime|'><around*|(|r|)>=h<around*|(|r|)>+\<Delta\>h<around*|(|r|)>>
    where <math|\<Delta\>h<around*|(|r|)>=<big|sum><rsub|s\<in\><with|math-font|cal|X>><around*|{|q<around*|(|s\<rightarrow\>r|)><around*|[|
    \<delta\><rsub|s\<in\>J<around*|(|r|)>>/p<around*|(|r|)>+\<delta\><rsub|s\<nin\>J<around*|(|r|)>>/p<around*|(|s|)>|]>|}>
    <around*|{|h<around*|(|s|)> p<around*|(|r|)>-h<around*|(|r|)>
    p<around*|(|s|)>|}>>. Thus, we have <math|<around*|{|r<rsub|2>,r<rsub|3>,\<ldots\>,r<rsub|N>|}>\<sim\>h<rprime|'>>.
    That is, the histogram of <math|<around*|{|r<rsub|2>,r<rsub|3>,\<ldots\>,r<rsub|N>|}>>,
    after normalization, can be fitted by <math|h<rprime|'>>. Combining the
    two sides, we have <math|h<rprime|'>\<approx\>h> on
    <math|<with|math-font|cal|X>>.

    Next is to proof that <math|h<rprime|'>=h\<Rightarrow\>h=p> on
    <math|<with|math-font|cal|X>>. This proof temporally employs the
    Perron\UFrobenius theorem. As in the proof of lemma <reference|lemma:
    transition>, before inserting the condition
    <math|q<around*|(|s\<rightarrow\>r|)>=q<around*|(|r\<rightarrow\>s|)>>,

    <\eqnarray*>
      <tformat|<table|<row|<cell|h<rprime|'><around*|(|r|)>>|<cell|=>|<cell|h<around*|(|r|)>>>|<row|<cell|>|<cell|+>|<cell|<big|sum><rsub|s\<in\>J<around*|(|r|)>>
      h<around*|(|s|)> q<around*|(|s\<rightarrow\>r|)>+<big|sum><rsub|s\<nin\>J<around*|(|r|)>>
      h<around*|(|s|)> q<around*|(|s\<rightarrow\>r|)>
      <frac|p<around*|(|r|)>|p<around*|(|s|)>>>>|<row|<cell|>|<cell|->|<cell|<big|sum><rsub|s\<in\>J<around*|(|r|)>>
      h<around*|(|r|)> q<around*|(|r\<rightarrow\>s|)>
      <frac|p<around*|(|s|)>|p<around*|(|r|)>>-<big|sum><rsub|s\<nin\>J<around*|(|r|)>>
      h<around*|(|r|)> q<around*|(|r\<rightarrow\>s|)>>>|<row|<cell|>|<cell|\<assign\>>|<cell|<big|sum><rsub|s\<in\><with|math-font|cal|X>>
      K<around*|(|r,s|)> h<around*|(|s|)>,>>>>
    </eqnarray*>

    where

    <\eqnarray*>
      <tformat|<table|<row|<cell|K<around*|(|r,s|)>>|<cell|=>|<cell|\<delta\><rsub|s\<in\>J<around*|(|r|)>>
      q<around*|(|s\<rightarrow\>r|)>+\<delta\><rsub|s\<nin\>J<around*|(|r|)>>
      q<around*|(|s\<rightarrow\>r|)> <frac|p<around*|(|r|)>|p<around*|(|s|)>>
      >>|<row|<cell|>|<cell|+>|<cell|\<delta\><rsub|r,s>\<times\><around*|[|1-<big|sum><rsub|t\<in\>J<around*|(|r|)>>
      q<around*|(|r\<rightarrow\>t|)> <frac|p<around*|(|t|)>|p<around*|(|r|)>>-<big|sum><rsub|t\<nin\>J<around*|(|r|)>>q<around*|(|r\<rightarrow\>t|)>|]>.>>>>
    </eqnarray*>

    Or in matrix form <math|\<b-h\>=K \<b-h\>>. That is, <math|\<b-h\>> is
    the eigen-vector of <math|K> with eigen-value <math|1>.

    Since, for <math|\<forall\>t\<in\>J<around*|(|r|)>>,
    <math|0\<less\>p<around*|(|t|)>/p<around*|(|r|)>\<leqslant\>1>, we have

    <\eqnarray*>
      <tformat|<table|<row|<cell|>|<cell|>|<cell|1-<big|sum><rsub|t\<in\>J<around*|(|r|)>>
      q<around*|(|r\<rightarrow\>t|)> <frac|p<around*|(|t|)>|p<around*|(|r|)>>-<big|sum><rsub|t\<nin\>J<around*|(|r|)>>q<around*|(|r\<rightarrow\>t|)>>>|<row|<cell|>|<cell|\<geqslant\>>|<cell|1-<big|sum><rsub|t\<in\>J<around*|(|r|)>>
      q<around*|(|r\<rightarrow\>t|)>-<big|sum><rsub|t\<nin\>J<around*|(|r|)>>q<around*|(|r\<rightarrow\>t|)>>>|<row|<cell|>|<cell|=>|<cell|1-1=0;>>>>
    </eqnarray*>

    also since, for <math|\<forall\>r,s\<in\><with|math-font|cal|X>>, both
    <math|q<around*|(|s\<rightarrow\>r|)>> and <math|p<around*|(|r|)>> are
    positive, we thus conclude that, for <math|\<forall\>r,s\<in\><with|math-font|cal|X>>

    <\equation*>
      K<around*|(|r,s|)>\<gtr\>0,
    </equation*>

    that is, <math|K> is a positive real square matrix. Recall
    <hlink|Perron\UFrobenius theorem for positive
    matrices|https://en.wikipedia.org/wiki/Perron\UFrobenius_theorem#No_other_non-negative_eigenvectors>
    states that ``given positive matrix<\footnote>
      I.e. positive real squre matrix.
    </footnote> <with|font-shape|italic|A>, the Perron\UFrobenius
    eigenvector<\footnote>
      I.e. that unique eigen-vector (up to multiplication by constant) of the
      Perron-Frobenius eigen-value, which is defined
      <hlink|herein|https://en.wikipedia.org/wiki/Perron\UFrobenius_theorem#Positive_matrices>.
    </footnote> is the only (up to multiplication by constant) non-negative
    eigenvector for <with|font-shape|italic|A>''. As in corollary
    <reference|corollary: Existence of Stable Distribution>, by letting
    <math|\<b-h\>=\<b-p\>>, we have gained an eigen-value of <math|K> such
    that all components are real and non-negative. So, as a distribution
    (thus all components have to be real and non-negative), <math|\<b-h\>>
    has no choice but be <math|\<b-p\>>, which is what we want to prove.
  </proof>

  <\remark>
    [Burn-in]

    Within this intuitive proof, we have to ensure that dropping
    <math|r<rsub|1>> from <math|<around*|{|r<rsub|1>,r<rsub|2>,\<ldots\>,r<rsub|N-1>|}>>
    affects little on the fitting of <math|h>. This does affect <math|h> if
    <math|r<rsub|1>> happens to be the state where
    <math|p<around*|(|r|)>\<ll\>1>, so that causes a ``Poisson error''. After
    all, <math|r<rsub|1>> is initialized randomly. For this reason,
    ``burn-in'' mechanism is introduced in. While adding <math|r<rsub|N>>
    will affects little on <math|h<rprime|'>-h>, since the probability of
    being in the ``important region'' of <math|p> for <math|r<rsub|N>> is
    large, after all, <math|r<rsub|N>> is not initialized randomly as
    <math|r<rsub|1>>.
  </remark>
</body>

<initial|<\collection>
</collection>>

<\references>
  <\collection>
    <associate|algorithm: Metropolis|<tuple|1|?>>
    <associate|auto-1|<tuple|1|?>>
    <associate|corollary: Existence of Stable Distribution|<tuple|3|?>>
    <associate|firstHeading|<tuple|1|?>>
    <associate|footnote-1|<tuple|1|?>>
    <associate|footnote-2|<tuple|2|?>>
    <associate|footnote-3|<tuple|3|?>>
    <associate|footnote-4|<tuple|4|?>>
    <associate|footnote-5|<tuple|5|?>>
    <associate|footnr-1|<tuple|1|?>>
    <associate|footnr-2|<tuple|2|?>>
    <associate|footnr-3|<tuple|3|?>>
    <associate|footnr-4|<tuple|4|?>>
    <associate|footnr-5|<tuple|5|?>>
    <associate|lemma: transition|<tuple|2|?>>
    <associate|theorem: Metropolis|<tuple|4|?>>
  </collection>
</references>