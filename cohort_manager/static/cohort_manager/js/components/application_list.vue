<template>
  <div>
    <div v-if="applicationReturn === 'Assigned'">
      <b-table
        responsive
        striped
        show-empty
        small
        class="aat-data-table"
        :items="applications"
        :fields="applicationFields"
      >
        <template v-slot:cell(Class)="row">
          <div>{{ row.value.quarter }} {{ row.value.year }}</div>
        </template>
      </b-table>
    </div>

    <div v-else-if="applicationReturn === 'Protected'">
      <b-table
        responsive
        striped
        show-empty
        small
        class="aat-data-table"
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
      </b-table>
    </div>


    <div v-else-if="applicationReturn === 'Duplicate'">
      <b-table
        responsive
        striped
        show-empty
        small
        class="aat-data-table"
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
        selected: {},
        to_remove: [],
        applicationFields: [
          {
            key: 'Key',
            label: "System Key",
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: true
          },
          {
            key: 'Type',
            label: "Application Type",
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: true
          },
          {
            key: 'Status',
            class: "aat-data-cell aat-data-nowrap",
            thClass: "aat-table-header",
            sortable: true
          },
          {
            key: 'Class',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: true
          },
          {
            key: 'Campus',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: true
          },
          {
            key: 'Cohort',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: true
          },
          {
            key: 'Major',
            class: "aat-data-cell aat-data-nowrap",
            thClass: "aat-table-header",
            sortable: true
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
            sortable: true
          },
          {
            key: 'admission_selection_id',
            label: "AdSel ID",
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: true
          },
          {
            key: 'application_number',
            label: "Application #",
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'Type',
            label: "Application Type",
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'Status',
            class: "aat-data-cell aat-data-nowrap",
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
            key: 'campus',
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
        var vue = this;
        this.to_remove = [];
        $.each(this.selected, function (idx, selected) {
          if (selected === false) {
            vue.to_remove.push(idx);
          }
        });
        this.$emit("dupeToRemove", this.to_remove);
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
