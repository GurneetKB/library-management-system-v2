<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header text-center bg-primary text-white">
            <h3 class="mb-0">Sign Up</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="signUp">
              <div class="mb-3">
                <label for="name" class="form-label">Name:</label>
                <input type="text" id="name" class="form-control" v-model="name" required>
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" id="email" class="form-control" v-model="email" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input type="password" id="password" class="form-control" v-model="password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100">Sign Up</button>
            </form>
            <div class="text-center mt-2" v-if="message">{{ message }}</div>
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
      name: '',
      email: '',
      password: '',
      message: ''
    };
  },
  methods: {
    signUp() {
      const userData = {
        name: this.name,
        email: this.email,
        password: this.password
      };
      // Make API call to Flask backend for sign-up
      fetch('http://localhost:5000/api/usersignup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      })
      .then(response => response.json())
      .then(data => {
        this.message = data.message;
        this.$router.push('/');
      })
      .catch(error => {
        console.error('Error:', error);
        this.message = 'An error occurred during sign up.';
      });
    }
  }
};
</script>
