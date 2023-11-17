---
title: React/React Native Http Interceptor.
author: csr13
description: Http Interceptor for React Native applications.
date: 2023-11-13
permalink: /pages/posts/http-interceptor-react.html
categories: react
            http
            best-practice
---

When developing user based mobile application or web applications and using JWTokens
for authentication, there is the need to always return the user when the backend
returns a not authenticated response -- wether is to do a token refresh or a session
expiration action e.g: session token expires user needs to log in again.


This is a simple http interceptior that can be used when developing Mobile
Applications and Web Applications that handle user actions e.g: social media.

`AuthService` has some helper methods, self explanatory.

```javascript
import axios from "axios";
import AuthService from "./auth.service";

const redirect = (url, clear = false) => {
  if (clear) {
    window.localStorage.clear();
  }
  window.location.href = url;
};

const token_expired = () => {
  var user = AuthService.decode_user();
  if (!user.exp) {
    redirect("/login", false);
  }
  if (new Date(user.exp * 1000) < new Date()) {
    return true;
  }
  return false;
};

const Interceptor = axios.interceptors.response.use(
  (response) => {
    if (token_expired()) {
      redirect("/login", true);
    }

    if (response.status === 401) {
      redirect("/login", true);
    } else if (response.status === 403) {
      redirect("/login", true);
    }
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      redirect("/login", true);
    } else if (error.response && error.response.status === 403) {
      redirect("/login", true);
    }
    return error;
  }
);

export default Interceptor;
```
