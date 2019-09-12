<template>
  <div>
        <b-modal :id="resetModal.id" :title="resetModal.title" ok-only @hide="resetresetModal">
          <div>This is {{collectionType}} {$(item.CohortNum)}</div>
        </b-modal>
    </div>
</template>

<script>
  export default {
    name: "collectionReset",
    components: {
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },

    },
    data(){
      return {
        resetModal: {
          id: 'reset-modal',
          title: ''
        }
      };
    },
    mounted() {
    },
    methods: {
      info(item, index, button) {
        this.resetModal.title = `Reset Cohort ${item.cohortNum}`
        this.resetModal.content = ``
        this.$root.$emit('bv::show::modal', this.resetModal.id, button)
      },
      resetresetModal() {
        this.resetModal.title = ''
        this.resetModal.content = ''
      },
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

</style>
