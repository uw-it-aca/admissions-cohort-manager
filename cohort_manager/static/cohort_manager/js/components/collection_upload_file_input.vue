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
        file_data: undefined,
        file_invalid_msg: undefined,
        file_name: undefined
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
        this.file_name = file.name;
        var contents,
            parsed_contents;
        const reader = new FileReader();
        reader.addEventListener('load', (event) => {
          contents = event.target.result;
          parsed_contents = this.parseCSV(contents);
          if(this.validateFileData(parsed_contents)){
            this.emitError(this.file_invalid_msg);
          } else{
            this.file_data = parsed_contents;
          }
        });
        reader.readAsText(file);
      },
      parseCSV(csv_data) {
        try {
          const results = parse(csv_data, {
            columns: true,
            skip_empty_lines: true,
          });
          return results;
        } catch(err){
          this.emitError("Could not parse file, expecting tab separated data. " + err);
        }
      },
      emitError(err){
        this.$emit('fileerror', err);
      },
      emitSyskeys(){
        var syskeys = this.file_data.map(a => parseInt(a.SDBSrcSystemKey));
        this.$emit('fileuploaded', {'syskeys': syskeys,
                                    'filename': this.file_name});
      },

      validateFileData(data) {
        var row_missing_key = false,
            row_missing_value = false,
            missing_data = false;

        if(data.length === 0){
          missing_data = true;
          this.file_invalid_msg = "File does not contain data";
        }
        for (const row of data){
          if (!('SDBSrcSystemKey' in row)){
            row_missing_key = true;
            this.file_invalid_msg = "File missing column: SDBSrcSystemKey";
          }else if(row['SDBSrcSystemKey'].length === 0){
            row_missing_value = true;
            this.file_invalid_msg = "One or more rows are missing an SDBSrcSystemKey";
          }
        }
        return row_missing_key || row_missing_value || missing_data;
      },
    },
  };
</script>

<style lang="scss">
</style>
