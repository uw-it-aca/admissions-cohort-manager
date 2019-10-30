<template>
  <b-form-file id="file"
               ref="file"
               v-model="file_upload"
               :state="Boolean(file_upload)"
               placeholder="Choose a file or drop it here..."
               drop-placeholder="Drop file here..."
               class="aat-file-input is-invalid"
               required
  />
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
