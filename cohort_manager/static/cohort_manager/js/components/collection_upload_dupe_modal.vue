<template>
  <b-modal
    id="dupe_list_modal"
    ref="dupe_modal"
    modal-class="aat-modal-box" content-class="aat-modal"
    hide-backdrop
    title="Duplicate Applications Found"
    ok-title="Done"
    :no-close-on-backdrop="true"
    :no-close-on-esc="true"
    :hide-header-close="true"
    :ok-only="true"
    @ok="removeDupes"
  >
    <div>
      <b-card-text>
        Select the applications that you want to assign:
      </b-card-text>
      <b-card-text>
        <applicationlist
          application-return="Duplicate"
          :collection-type="collectionType"
          :applications="duplicates"
          @dupe-to-remove="dupeManager"
        />
      </b-card-text>
    </div>
  </b-modal>
</template>

<script>
  import ApplicationList from "../components/application_list.vue";
  export default {
    name: "CollectionUploadDupeModal",
    components: {
      applicationlist : ApplicationList
    },
    props: {
      duplicates: {
        type: Array,
        default: function () {return[];}
      },
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
        to_keep: []
      };
    },
    computed: {
      to_remove: function() {
        var applications = [],
            vue = this;
        $(this.duplicates).each(function (idx, val) {
          if(!vue.to_keep.includes(val.admission_selection_id)){
            applications.push(val.admission_selection_id);
          }
        });
        return applications;
      }
    },
    mounted() {
      this.$refs.dupe_modal.show();
    },
    methods: {
      dupeManager(list) {
        // Something is causing this to fire when modal closes,
        // ignore that object
        if(Array.isArray(list)){
          this.to_keep = list;
        }
        return;
      },
      removeDupes(){
        this.$emit('remove-dupes', this.to_remove);
      }
    }
  };
</script>

<style lang="scss">
</style>
