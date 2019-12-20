<template>
  <b-container fluid>
    <b-row>
      <b-col>
        <b-pagination
          v-if="totalRows > perPage"
          v-model="currentPage"
          class="aat-activity-pagination"
          :total-rows="totalRows"
          :per-page="perPage"
          size="sm"
          aria-controls="assignment_history_table"
        />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12" class="aat-col-nopad aat-activity-table">
        <b-table
          id="assignment_history_table"
          hover
          responsive
          show-empty
          striped
          small
          class="aat-data-table"
          :items="activities"
          :fields="activityFields"
          :current-page="currentPage"
          :per-page="perPage"
          :filter="filter"
        >
          <template v-slot:cell(assigned_msg)="row">
            {{row.item.assigned_msg}} applications to <span v-if="row.item.cohort">Cohort {{row.item.cohort}}</span><span v-if="row.item.major">{{row.item.major}}</span>
          </template>
          <template v-slot:cell(submitted_msg)="row">
            Attempted {{row.item.submitted_msg}} applications to <span v-if="row.item.cohort">Cohort {{row.item.cohort}}</span><span v-if="row.item.major">{{row.item.major}}</span>
          </template>
          <template v-slot:cell(selection)="row">
            <a href="https://www.tableau.com" :title="'View filters in Tableau'"><i class="fas fa-filter" /><span class="sr-only">Filters</span></a>
          </template>
        </b-table>
      </b-col>
    </b-row>
  </b-container>
</template>



<script>
  const axios = require("axios");
  export default {
    name: "ActivityList",
    components: {
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
        activityFields: [
          {
            key: 'activity_date',
            label: "Date/Time",
            class: "aat-data-cell aat-data-nowrap",
            thClass: "aat-table-header",
            sortable: true,
          },
          {
            key: 'assigned_msg',
            label: 'Assignment',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false
          },
          {
            key: 'submitted_msg',
            label: 'Submitted',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false
          },
          {
            key: 'selection',
            class: "aat-data-cell aat-filters-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'comment',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: false,
          },
          {
            key: 'user',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: true,
          },
        ],
        activities: [],
        cohortFilter: null,
        cohortOptions: [],
        majorFilter: null,
        majorOptions: [],
        syskeyFilter: null,
        totalRows: 1,
        currentPage: 1,
        perPage: 20,
        filter: null,
        filterOn: [],
      };
    },
    mounted() {
      // Set the initial number of items
      this.totalRows = this.activities.length;
      this.getAllActivities();
      this.selectCollection(this.$route.params.id);
    },
    methods: {
      onFiltered(filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.totalRows = filteredItems.length;
        this.currentPage = 1;
      },
      onReset(evt) {
        evt.preventDefault();
        // Reset our form values
        this.cohortFilter = null;
        this.majorFilter = null;
        this.syskeyFilter = '';
        // Trick to reset/clear native browser form validation state
        this.show = false;
        this.$nextTick(() => {
          this.show = true;
        });
      },
      getMajorActivities(major_id){
        this.getActivities("?major_id=" + major_id);
      },
      getCohortActivities(cohort_id){
        this.getActivities("?cohort_id=" + cohort_id);
      },
      getSyskeyActivities(syskey){
        this.getActivities("?system_key=" + syskey);
      },
      getAllActivities() {
        this.getActivities("");
      },
      getActivities(filter_string){
        axios.get(
          '/api/activity/' + filter_string,
        ).then(response => {
          if(response.status === 200){
            this.activities = response.data.activities;
            this.totalRows = this.activities.length;
          }
        });
      },
      selectCollection(id){
        var id_to_set;
        if(isNaN(id) && id !== undefined){
          $(this.majorOptions).each(function(idx, option){
            if (id.toLowerCase() === option.value.toLowerCase()){
              id_to_set = id;
            }
          });
          if (id_to_set !== undefined){
            this.majorFilter = id_to_set.toLowerCase();
          }
        } else{
          $(this.cohortOptions).each(function(idx, option){
            if (id === option.value){
              id_to_set = id;
            }
          });
          if (id_to_set !== undefined){
            this.cohortFilter = id_to_set;
          }
        }
      }
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';

  // general layout
  .aat-col-nopad {
    padding: 0;
  }

  // filters and pagination
  .aat-activity-pagination {
    float: right;
  }

  .aat-filter-form {
    border-top: 1px solid $table-border;
    margin-bottom: 3rem;
  }

  .aat-filter-title {
    float: left;
    font-size: 1rem;
    font-weight: bold;
    line-height: inherit;
  }

  .aat-filter-reset button {
    float: right;
    font-size: 0.875rem;
    line-height: 1.7;
    padding: 0 0 0 0.5rem;
    text-transform: lowercase;
  }

  //table
  .aat-filters-cell {
    text-align: center;
    vertical-align: middle !important;
  }

</style>
