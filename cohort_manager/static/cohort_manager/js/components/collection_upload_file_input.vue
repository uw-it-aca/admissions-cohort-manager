<template>
  <b-form-file :state="Boolean(file)" placeholder="Choose a file or drop it here..." drop-placeholder="Drop file here..." id="file" ref="file" class="aat-file-input" @change="selectedFile">
  </b-form-file>
</template>

<script>
  export default {
    name: "CollectionUploadFileInput",
    components: {},
    props: {},
    data(){
      return {
        file: ''
      };
    },
    watch: {},
    mounted() {
    },
    methods: {
      selectedFile() {
        this.file = this.$refs.file.files[0];
        this.$emit('fileselected', this.file);
      }

    },
  };
</script>

<style lang="scss">
</style>
