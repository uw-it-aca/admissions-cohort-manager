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
      <b-col cols="12" order="2" class="aat-col-nopad aat-activity-table">
        <b-table
          id="assignment_history_table"
          hover
          responsive
          show-empty
          striped
          small
          class="aat-data-table"
          :busy="is_loading"
          :items="activities"
          :fields="activityFields"
          :current-page="currentPage"
          :per-page="perPage"
          :filter="filter"
        >
          <template v-slot:cell(activity_date)="row">
            {{ row.item.activity_date | moment("timezone", "America/Los_Angeles", "MMM DD, YYYY") }}<br>{{ row.item.activity_date | moment("timezone", "America/Los_Angeles", "h:mm A") }}
          </template>
          <template v-slot:cell(assigned_msg)="row">
            {{ row.item.assigned_msg }} {{ 'application' | pluralize(row.item.assigned_msg) }} to <span v-if="row.item.major !== null">{{ row.item.major }}</span><span v-else>Cohort {{ row.item.cohort }}</span>
          </template>
          <template v-slot:cell(submitted_msg)="row">
            Attempted {{ row.item.submitted_msg }} {{ 'application' | pluralize(row.item.submitted_msg) }} to <span v-if="row.item.major !== null">{{ row.item.major }}</span><span v-else>Cohort {{ row.item.cohort }}</span>
          </template>
          <template v-slot:table-busy>
            <div class="text-center text-info">
              <b-spinner class="align-middle" />
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>

      <b-col order="1" class="aat-filter-container">
        <b-form class="aat-filter-form" @reset="onReset">
          <b-row>
            <b-col cols="12">
              <h2 class="aat-filter-title">
                Filter
              </h2>
              <span class="aat-filter-reset">
                <b-button type="reset" variant="link" @click="getAllActivities">
                  Reset
                </b-button>
              </span>
              <span class="aat-filter-toggle">
                <b-button variant="link" v-b-toggle.aat_collapse_filter>
                    <span class="aat-filter-toggle-label sr-only">
                      Show Filters
                    </span>
                </b-button>
              </span>
            </b-col>
            <b-collapse id="aat_collapse_filter" class="aat-filter-collapse" cols="12"> 
              <b-row>
            <b-col cols="6">
              <b-form-group
                label="Collection Type"
                label-size="sm"
                label-for="collection_filter"
              >
                <b-input-group size="sm">
                  <b-form-select
                    id="collection_filter"
                    name="collectionType"
                    v-model="collectionFilter"
                    class="aat-filter-select"
                    :options="collectionOptions"
                    @change="getCollectionActivities"
                  >
                    <template v-slot:first>
                      <option :value="null">
                        All Collection Types
                      </option>
                    </template>
                  </b-form-select>
                </b-input-group>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group
                label="Assignment Type"
                label-size="sm"
                label-for="assignment_filter"
              >
                <b-input-group size="sm">
                  <b-form-select
                    id="assignment_filter"
                    v-model="assignmentFilter"
                    class="aat-filter-select"
                    :options="assignmentOptions"
                    @change="getAssignmentActivities"
                  >
                    <template v-slot:first>
                      <option :value="null">
                        All Assignments
                      </option>
                    </template>
                  </b-form-select>
                </b-input-group>
              </b-form-group>
            </b-col>
            <b-col cols="6" v-if= "collectionFilter === 'cohort' || collectionFilter === null">
              <b-form-group
                label="Cohort"
                label-size="sm"
                label-for="cohort_filter"
              >
                <b-input-group size="sm">
                  <b-form-select
                    id="cohort_filter"
                    v-model="cohortFilter"
                    class="aat-filter-select"
                    :options="cohortOptions"
                    @change="getCohortActivities"
                  >
                    <template v-slot:first>
                      <option :value="null">
                        All Cohorts
                      </option>
                    </template>
                  </b-form-select>
                </b-input-group>
              </b-form-group>
            </b-col>
            <b-col cols="6" v-if= "collectionFilter === 'major' || collectionFilter === null">
              <b-form-group
                label="Major"
                label-size="sm"
                label-for="major_filter"
              >
                <b-input-group size="sm">
                  <b-form-select
                    id="major_filter"
                    v-model="majorFilter"
                    class="aat-filter-select"
                    :options="majorOptions"
                    @change="getMajorActivities"
                  >
                    <template v-slot:first>
                      <option :value="null">
                        All Majors
                      </option>
                    </template>
                  </b-form-select>
                </b-input-group>
              </b-form-group>
            </b-col>
            <b-col cols="12" sm="6">
              <b-form-group
                label="User"
                label-size="sm"
                label-for="user_filter"
              >
                <b-input-group size="sm">
                  <b-form-select
                    id="user_filter"
                    v-model="userFilter"
                    class="aat-filter-select"
                    :options="userOptions"
                    @change="getUserActivities"
                  >
                    <template v-slot:first>
                      <option :value="null">
                        All Users
                      </option>
                    </template>
                  </b-form-select>
                </b-input-group>
              </b-form-group>
            </b-col>
            <b-col cols="12" sm="6">
              <b-form-group
                label="System Key or AdSelect ID"
                label-size="sm"
                label-for="SysKeyInput"
              >
                <b-input-group size="sm">
                  <b-form-input
                    id="SysKeyInput"
                    v-model="syskeyFilter"
                    placeholder="Type to Search"
                    @change="getSyskeyActivities"
                  />
                </b-input-group>
              </b-form-group>
            </b-col>
            <b-col cols="12">
              <b-form-group
                label="Search Comment Text"
                label-size="sm"
                label-for="CommentInput"
              >
                <b-input-group size="sm">
                  <b-form-input
                    id="CommentInput"
                    v-model="commentFilter"
                    placeholder="Type to Search"
                    @change="getCommentActivities"
                  />
                </b-input-group>
              </b-form-group>
            </b-col>
              </b-row>
          </b-collapse>
          </b-row>
        </b-form>
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
            label: 'Assigned',
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
            key: 'collection_type',
            label: 'Type',
            class: "aat-data-cell",
            thClass: "aat-table-header",
            sortable: true
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
        collectionFilter: null,
        collectionOptions: [
          { value: 'cohort', text: 'Cohort' },
          { value: 'major', text: 'Major' },
          { value: 'pg', text: 'P & G' }
        ],
        cohortFilter: null,
        cohortOptions: [
          { value: '1', text: '1' },
          { value: '2', text: '2' },
          { value: '3', text: '3' },
          { value: '99', text: '99' }
        ],
        majorFilter: null,
        majorOptions: [
          { value: 'astr', text: 'ASTR' },
          { value: 'biol', text: 'BIOL' },
          { value: 'cse', text: 'CSE' },
          { value: 'hcde', text: 'HCDE' }
        ],
        syskeyFilter: null,
        commentFilter: null,
        userFilter: null,
        userOptions: [
          { value: 'asmith', text: 'asmith' },
          { value: 'bsmith', text: 'bsmith' },
          { value: 'csmith', text: 'csmith' }
        ],
        assignmentFilter: null,
        assignmentOptions: [
          { value: 'file', text: 'File' },
          { value: 'manual', text: 'Manual' },
          { value: 'Tableau', text: 'Tableau' }
        ],
        totalRows: 1,
        currentPage: 1,
        perPage: 20,
        filter: null,
        filterOn: [],
        is_loading: true
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
        this.collectionFilter = null;
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
        this.is_loading = true;
        axios.get(
          '/api/activity/' + filter_string,
        ).then(response => {
          if(response.status === 200){
            this.activities = response.data.activities;
            this.totalRows = this.activities.length;
          }
          this.is_loading = false;
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
  .aat-filter-collapse {
    padding: 0 15px;
  }

  .aat-activity-pagination {
    float: right;
  }

  .aat-filter-form {
    border-top: 1px solid $table-border;
    margin-bottom: 1rem;
  }

  .aat-filter-title {
    float: left;
    font-size: 1rem;
    font-weight: bold;
    line-height: inherit;
  }

  .aat-filter-reset button {
    float: left;
    font-size: 0.875rem;
    line-height: 1.7;
    padding: 0 0 0 0.5rem;
    text-transform: lowercase;
  }

  .aat-filter-toggle button {
    float: right;
    font-size: 0.875rem;
    height: 1rem;
    line-height: 1.7;
    margin-top: 0.3rem;
    padding: 0 0 0 0.5rem;
    text-transform: lowercase;
    width: 1rem;
  }

  .aat-filter-toggle button::after {
    border-style: solid;
    border-width: 0 2px 2px 0;
    content: '';
    padding: 2px;
    position: absolute;
    right: 20px;
    top: 0.6rem;
    transform: rotate(-45deg);
    transition: transform 0.5s;
  }

  .aat-filter-toggle .btn.not-collapsed::after {
    transform: rotate(45deg);
  }

  //table
  .aat-filters-cell {
    text-align: center;
    vertical-align: middle !important;
  }

</style>
