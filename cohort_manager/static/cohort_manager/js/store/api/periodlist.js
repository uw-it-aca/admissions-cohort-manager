const state = {
  periods: []
};

// getters
const getters = {
  periods: state => {
    return state.periods;
  }
};

// actions
const actions = {
  get_periods ({ commit }) {
    this.$axios.get(`/api/periods/`)
      .then(response => response.data)
      .then(items => {
        commit('set_periods', items);
      });
  }
};

// mutations
const mutations = {
  set_periods (state, periods) {
    for (var period of periods){
      period.text = period.text + " - " + period.value;
    }
    state.periods = periods;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
