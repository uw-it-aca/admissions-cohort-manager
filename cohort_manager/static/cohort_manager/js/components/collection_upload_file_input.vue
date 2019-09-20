<template>
  <input id="file" ref="file" type="file" class="aat-file-input" @change="selectedFile">
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
