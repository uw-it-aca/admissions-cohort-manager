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
    name: "PurpleGoldUploadFileInput",
    components: {},
    props: {},
    data(){
      return {
        file_upload: undefined,
        file: undefined,
        file_data: undefined,
        file_invalid_msg: undefined
      };
    },
    watch: {
      file_upload: function(file){
        this.selectedFile(file);
      },
      file_data: function(){
        this.emitAwards();
      }
    },
    mounted() {
    },
    methods: {
      selectedFile(file) {
        this.file = file;
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
            delimiter: ","
          });
          return results;
        } catch(err){
          this.emitError("Could not parse file, expecting tab separated data. " + err);
        }
      },
      emitError(err){
        this.$emit('fileerror', err);
      },
      emitAwards(){
        this.$emit('fileuploaded', this.file_data);
      },

      validateFileData(data) {
        var has_error = false;
        if(data.length === 0){
          this.file_invalid_msg = "File does not contain data";
          has_error = true;
        }
        for (const row of data){
          if(this.missingValue(row, "admissionSelectionID") ||
            this.missingValue(row, "awardAmount")
          ){
            has_error = true;
          }

        }
        return has_error;
      },

      missingValue(data, value){
        var missingValue = false;
        if (!(value in data)){
          missingValue = true;
          this.file_invalid_msg = "File missing column: " + value;
        }else if(data['admissionSelectionID'].length === 0){
          missingValue = true;
          this.file_invalid_msg = "One or more rows are missing an " + value;
        }
        return missingValue;
      }
    },
  };
</script>

<style lang="scss">
</style>
