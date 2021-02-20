<template>
  <b-form-file id="file"
               ref="file"
               v-model="file_upload"
               accept=".csv"
               :state="Boolean(file_upload)"
               placeholder="Choose a file or drop it here..."
               drop-placeholder="Drop file here..."
               class="aat-file-input is-invalid"
               required
  />
</template>

<script>
  const parse = require("csv-parse/lib/sync");
  export default {
    name: "CollectionUploadFileInput",
    components: {},
    props: {},
    data(){
      return {
        file_upload: undefined,
        file: undefined,
        file_data: undefined
      };
    },
    watch: {
      file_upload: function(file){
        this.selectedFile(file);
      },
      file_data: function(){
        this.emitSyskeys();
      }
    },
    mounted() {
    },
    methods: {
      selectedFile(file) {
        this.file = file;
        var contents;
        const reader = new FileReader();
        reader.addEventListener('load', (event) => {
          contents = event.target.result;
          this.file_data = this.parseCSV(contents);
        });
        reader.readAsText(file);
      },
      parseCSV(csv_data) {
        const results = parse(csv_data, {
          columns: true,
          skip_empty_lines: true,
          delimiter: "\t"
        });
        return results;
      },
      emitSyskeys(){
        var syskeys = this.file_data.map(a => parseInt(a.SDBSrcSystemKey));
        this.$emit('fileuploaded', syskeys);
      }
    },
  };
</script>

<style lang="scss">
</style>
