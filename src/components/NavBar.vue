<template>
  <div>
    <b-navbar variant="light" toggleable="lg" fixed="top">
      <b-navbar-brand class="mx-5" to="/">{{ appName }}</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>

        <b-navbar-nav class="ms-auto">

          <b-nav-item class="mx-3">
            <router-link to="/documentation">
              <b-button variant="outline-secondary">Docs</b-button>
            </router-link>
          </b-nav-item>

          <b-nav-item class="mx-3">
            <router-link to="/about">
              <b-button variant="outline-secondary">About</b-button>
            </router-link>
          </b-nav-item>

          <b-nav-item v-if="$store.state.loggedIn" class="mx-3">
            <router-link to="/profile">
              <b-button variant="outline-secondary">Profile</b-button>
            </router-link>
          </b-nav-item>

          <b-nav-item v-if="!$store.state.loggedIn" class="mx-3" href="/login">
            <b-button variant="primary">Login</b-button>
          </b-nav-item>

          <b-nav-item v-if="$store.state.loggedIn" class="mx-3" href="/logout">
            <b-button variant="outline-primary">Logout</b-button>
          </b-nav-item>

        </b-navbar-nav>

      </b-collapse>

    </b-navbar>

    <!-- Banner alert for Alpha Mode if applicable -->
    <div v-if="alphaMode==='1'">
      <br/><br/>
      <b-alert class="text-center" show>
        <h5>{{ appName }} is currently in Alpha.</h5> We welcome your feedback.
      </b-alert>
    </div>
    <!-- End banner alert -->

    <!-- Banner alert for Beta Mode if applicable -->
    <div v-if="betaMode==='1'">
      <br/><br/>
      <b-alert class="text-center" show>
        <h5>{{ appName }} is currently in Beta.</h5> We welcome your feedback.
      </b-alert>
    </div>
    <!-- End banner alert -->

  </div>
</template>

<script>
export default {
  name: "NavBar",
  components: { },
  data() {
    return {
      appName: process.env.VUE_APP_NAME,
      alphaMode: process.env.VUE_APP_ALPHA_MODE,
      betaMode: process.env.VUE_APP_BETA_MODE,
    }
  },
  created() {
    this.$store.dispatch('refreshUserInfo')
  },
  methods: {  }
}
</script>
