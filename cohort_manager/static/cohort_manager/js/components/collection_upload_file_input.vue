<template>
  <b-form-file :state="Boolean(file_upload)"
               placeholder="Choose a file or drop it here..."
               drop-placeholder="Drop file here..."
               id="file"
               ref="file"
               class="aat-file-input"
               v-model="file_upload">
  </b-form-file>
</template>

<script>
  export default {
    name: "CollectionUploadFileInput",
    components: {},
    props: {},
    data(){
      return {
        file_upload: undefined
      };
    },
    watch: {
      file_upload: function(file){
        this.$emit('fileselected', file);
      }
    },
    mounted() {
    },
    methods: {
    },
  };
</script>

<style lang="scss">
</style>
