const state = {
  majors: []
};

// getters
const getters = {
  majors: state => {
    return state.majors;
  }
};

// actions
const actions = {
  get_majors ({ commit }, quarter) {
    this.$axios.get(`/api/collection/major/${quarter}/`)
      .then(response => response.data)
      .then(items => {
        commit('set_majors', items);
      });
  }
};

// mutations
const mutations = {
  set_majors (state, majors) {
    state.majors = majors;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
