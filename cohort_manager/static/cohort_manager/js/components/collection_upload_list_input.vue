<template>
  <div>
    <p>Enter System Keys, one per line or separated by commas.</p>
    <textarea v-model="syskey_input" class="syskey-input" />
  </div>
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
    watch: {
      syskey_input: function(input){
        this.processList(input);
        this.$emit('listupdated', this.syskey_list);
      }
    },
    mounted() {
    },
    methods: {
      processList(text_contents) {
        var parsed = text_contents.replace(new RegExp(',', 'g'), " ");
        this.syskey_list = parsed.match(/[^\s]+/g);
      }
    },
  };
</script>

<style lang="scss">
  .syskey-input {
    width: 100%;
  }   
</style>
