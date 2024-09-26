<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h3 class="mb-0">User Login</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="loginUser">
              <div class="mb-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" id="email" class="form-control" v-model="email" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input type="password" id="password" class="form-control" v-model="password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {

    async loginUser() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/userlogin", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });
        response.data = await response.json();
        if (response.data.access_token) {
          localStorage.setItem('accessToken', response.data.access_token);
          localStorage.setItem('user', JSON.stringify(response.data.userName));
          this.$router.push('/user/dashboard');
          console.log(response.data.message);
        }
        else {
          alert(response.data.error);
        }
      } catch (error) {
        console.error("Error logging in:", error);
        alert(error.response.data.error);
      }
    },
  },
};
</script>
