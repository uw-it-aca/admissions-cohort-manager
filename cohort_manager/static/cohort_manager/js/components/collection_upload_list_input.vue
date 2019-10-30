<template>
  <b-modal id="add_list_modal" title="Add Applicantions" ok-title="Done" @ok="processList">
    <div>
      <p>Enter System Keys, one per line or separated by commas.</p>
      <textarea required v-model="syskey_input" class="is-invalid syskey-input" @ />
    </div>
  </b-modal>
</template>

<script>
  export default {
    name: "CollectionUploadListInput",
    components: {},
    props: {},
    data(){
      return {
        syskey_input: '',
        syskey_list: [],
      };
    },
    methods: {
      processList() {
        var parsed = this.syskey_input.replace(new RegExp(',', 'g'), " ");
        this.syskey_list = parsed.match(/[^\s]+/g);
        this.$emit('listupdated', this.syskey_list);
      }
    },
  };
</script>

<style lang="scss">

  // form fields
  .syskey-input {
    width: 100%;
  }
</style>
