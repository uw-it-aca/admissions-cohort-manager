<template>
  <div>
    <div v-if="applicationReturn === 'Assigned'">
      <b-table
        hover
        responsive
        show-empty
        small
        class="aat-data-table"
        :busy="isBusy"
        :items="applications"
        :fields="applicationFields"
      >
        <template v-slot:cell(Class)="row">
          <div>{{ row.value.quarter }} {{ row.value.year }}</div>
        </template>
        <template v-slot:table-busy>
          <div class="text-center text-info">
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </div>

    <div v-else-if="applicationReturn === 'Protected'">
      <b-table
        hover
        responsive
        show-empty
        small
        class="aat-data-table"
        :busy="isBusy"
        :items="applications"
        :fields="applicationFields"
      >
        <template v-slot:cell(actions)="row">
          <b-form-checkbox
            :id="'app_select_' + row.item.Key + '_' + row.item.Number"
            v-model="selected"
            :name="'app_select_' + row.item.Key + '_' + row.item.Number"
            value="selected"
            unchecked-value="not_selected"
          >
            <span class="sr-only">Select application {{ row.item.Key }}</span>
          </b-form-checkbox>
        </template>
        <template v-slot:cell(Class)="row">
          <div>{{ row.value.quarter }} {{ row.value.year }}</div>
        </template>
        <template v-slot:table-busy>
          <div class="text-center text-info">
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </div>


    <div v-else-if="applicationReturn === 'Duplicate'">
      <b-table
        hover
        responsive
        show-empty
        small
        class="aat-data-table"
        :busy="isBusy"
        :items="applications"
        :fields="appDupeFields"
      >
        <template v-slot:cell(actions)="row">
          <b-form-group>
            <b-form-checkbox
              :id="'app_select_' + row.item.admission_selection_id + '_' + row.item.application_number"
              :key="row.item.admission_selection_id"
              v-model="selected[row.item.admission_selection_id]"
              :name="'app_select_' + row.item.admission_selection_id + '_' + row.item.application_number"
              :value="true"
              @input="mark_to_delete"
            >
              <span class="sr-only">Select application {{ row.item.admission_selection_id }}</span>
            </b-form-checkbox>
          </b-form-group>
        </template>
        <template v-slot:cell(Class)="row">
          <div>{{ row.value.quarter }} {{ row.value.year }}</div>
        </template>
        <template v-slot:table-busy>
          <div class="text-center text-info">
            <b-spinner class="align-middle" />
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </div>
    <div v-else>
      <p>Error: We are missing something!</p>
    </div>
  </div>
</template>

<script>
  export default {
    name: "ApplicationList",
    components: {
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
      applicationReturn: {
        type: String,
        default: ""
      },
      applications: {
        type: Array,
        default: function() {return [];}
      },
    },
    data(){
      return {
        isBusy: false,
        selected: {},
        applicationFields: [
          {
            key: 'system_key',
            label: "System Key",
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'campus',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'assigned_cohort',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'description',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'protected',
            label: 'Protected',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'assigned_major',
            class: "aat-data-cell aat-data-nowrap",
            thClass: "aat-table-header",
            sortable: false,
          },
        ],

        appDupeFields: [
          {
            key: 'Actions',
            label: '',
            class: "aat-data-cell aat-app-select", },
          {
            key: 'system_key',
            label: "System Key",
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'application_number',
            label: "Application #",
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'Class',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'cohort',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'major',
            class: "aat-data-cell aat-data-nowrap",
            thClass: "aat-table-header",
            sortable: false,
          },
        ],


      };
    },
    watch: {
      applications: function (applications) {
        var vue = this;
        $.each(applications, function (idx, app) {
          vue.selected[app.admission_selection_id] = false;
        });
      },
    },
    mounted() {
    },
    methods: {
      mark_to_delete: function() {
        var keys_to_keep = [],
            keys_to_remove  = [],
            vue = this;
        $.each(vue.selected, function(key, value){
          if (value === true){
            keys_to_keep.push(key);
          }
        });
        $.each(vue.applications, function(idx, app){
          if(!keys_to_keep.includes(app.admission_selection_id)){
            keys_to_remove.push(app.admission_selection_id);
          }
        });
        this.$emit("dupeToRemove", keys_to_remove);
      }

    }
  };
</script>

<style lang="scss">

  // Table application selection
  .aat-data-cell {
    &.aat-app-select {
      padding: 0.75rem;
    }
  }
</style>
