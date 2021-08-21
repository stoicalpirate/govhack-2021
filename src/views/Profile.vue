<template>
  <div>
    <Layout>

      <div class="mb-5">
        <h1>Profile</h1>
        <br>
      </div>

      <div v-if="isLoading">
        <Loading />
      </div>

      <div v-else >

        <div class="my-5">
          <h4>Here are the topics and people you're currently tracking:</h4>
          <b-row>
            <b-col cols="4">
              <TopicList v-if="topicDataReceived" :sourceData="selectedTopicsData" @topicselected="setDisplayTopic"/>
              <Loading v-if="!topicDataReceived" />
            </b-col>
            <b-col>
              <!-- <StackedBarChart /> -->
            </b-col>
          </b-row>
        </div>

        <div class="my-5">
          <h4>Here are some other things you might like to track:</h4>
          <TopicList v-if="topicDataReceived" :sourceData="unselectedTopicsData" @topicselected="userFollowTopic"/>
          <Loading v-if="!topicDataReceived" />
        </div>

      </div>

    </Layout>
  </div>
</template>

<script>
import Layout from '../layouts/MainLayout'
import Loading from '../components/Loading'
import TopicList from '../components/TopicList.vue'

export default {
  page: {
    title: "Profile",
  },
  components: { Layout, Loading, TopicList },
  data() {
    return {
      isLoading: false,
      topicDataReceived: false,
      selectedTopicsData: [],
      unselectedTopicsData: [],
      topicToDisplay: null,
      userFollowTopicLoading: false
    }
  },
  mounted() {
    this.getTopicData()
  },
  methods: {
    async getTopicData() {
      this.$http
        .get("/api/user/topicdata")
        .then((response) => {
          this.selectedTopicsData = response.data.selected_topics
          this.unselectedTopicsData = response.data.unselected_topics
          this.topicDataReceived = true
        })
        .catch((error) => {
          console.log(error)
          this.topicDataReceived = true
        })
    },
    setDisplayTopic(topic) {
      this.topicToDisplay = topic
      console.log(this.topicToDisplay)
    },
    async userFollowTopic(topic) {
      this.userFollowTopicLoading = true
      const formData = new FormData()
      formData.append("selected_topic", topic)
      this.$http
        .post("/api/user/followtopic", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
        })
        .then((response) => {
          console.log(response)
          console.log("Topic is now being followed.")
          this.userFollowTopicLoading = false
        })
        .catch((error) => {
          console.log(error)
          this.userFollowTopicLoading = false
        })
    }
  }
}
</script>