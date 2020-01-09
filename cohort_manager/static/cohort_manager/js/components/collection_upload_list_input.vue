<template>
  <b-modal id="add_list_modal" modal-class="aat-modal-box" content-class="aat-modal" hide-backdrop title="Add Applications" ok-title="Done" @ok="processList" @shown="focusElement">
    <div>
      <p>Enter system keys, one per line or separated by commas.</p>
      <textarea ref="focusThis" v-model="syskey_input" required class="is-invalid syskey-input" @ />
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
      focusElement() {
        this.$refs.focusThis.focus();
      },
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
