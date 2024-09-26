<template>
    <UserNavbar />
    <div v-show="!isEditMode" class="container mt-4">
        <h1>User profile</h1>
        <img :src="image">

        <span>Name: </span><b id="name">{{ name }}</b>
        <hr />

        <span>Email: </span><b id="email">{{ email }}</b>
        <hr />

        <span>Interests: </span><b id="interests">{{ interests }}</b>
        <hr />

        <button @click="handleEditProfile">Edit Profile</button>
    </div>
    <div v-show="isEditMode" class="container mt-4">
        <h1>User profile</h1>
        <img :src="image">

        <span>Name: </span>
        <input type="text" id="input-name" v-model="name" />
        <hr />

        <span>Email: </span>
        <input type="text" id="input-email" v-model="email" />
        <hr />

        <span>Interests: </span>
        <input type="text" id="input-interests" v-model="interests" />
        <hr />

        <button @click="handleUpdateProfile">Update Profile</button>
    </div>
</template>

<script>
import image from "../assets/OIP.jpeg"
import UserNavbar from "../components/UserNavbar.vue";

export default {
    name: "UserProfile",
    components: {
        UserNavbar,
    },
    data() {
        return {
            image: image,
            id: "",
            name: "",
            email: "",
            interests: "",
            isEditMode: false

        }
    },
    async created() {
        const userData = await this.fetchUserProfile();
        this.id = userData.id
        this.name = userData.name
        this.email = userData.email
        this.interests = userData.Interests

    },

    methods: {
        handleEditProfile() {
            this.isEditMode = true
        },

        async handleUpdateProfile() {
            const payload = {
                id: this.id,
                name: this.name,
                email: this.email,
                interests: this.interests
            }
            const resJson = await this.updateUserProfile(payload)
            console.log(resJson)

            this.isEditMode = false
        },
        async fetchUserProfile() {
            const res = await fetch("http://127.0.0.1:5000/api/user/resource/manager", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            })
            return await res.json()
        },
        async updateUserProfile(payload) {
            const res = await fetch('http://127.0.0.1:5000/api/user/resource/manager', {
                method: "PUT",
                headers: {
                    'Content-type': 'application/json',
                    'Accept': 'application/json',
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
                body: JSON.stringify(payload)
            })
            return await res.json()
        }
    }
}
</script>

<style>
img {
    width: 300px;
    height: auto;
    display: block;
    margin-bottom: 40px;
}

hr {
    width: 400px;
    margin: 25px 0;
}

button {
    width: 160px;
    font-size: 15px;
    height: 45px;
    border-radius: 5px;
}

button:hover {
    cursor: pointer;
}

input {
    width: 200px;
    font-size: 15px;
    padding: 10px;
}
</style>