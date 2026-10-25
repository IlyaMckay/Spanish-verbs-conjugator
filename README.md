<!-- omit in toc -->
# **Conjugator**

> **Overview.** A web app for practicing Spanish verb conjugation, built under contract for a Spanish language school in 2024. It covers 2,000+ verbs across 29 tenses, with the three regional pronoun systems most conjugators skip (voseo, vosotros, sin voseo). I built the conjugation engine, a pipeline that extracts and normalizes verb lists from PDF and ODS sources into the database, and the Flask front end.
>
> **Status:** the hosted version is no longer online; the app runs locally (see Prerequisites below).
>
> **Stack:** Python · Flask · Gunicorn · TinyDB with custom ORM methods · TOML as a content store · BeautifulSoup

---

**Conjugator** is your reliable companion in learning Spanish. Try it out and see how mastering verb conjugations can be both enjoyable and simple.

<!-- omit in toc -->
## Table of Contents

- [Description](#description)
- [How to Use](#how-to-use)
  - [Page 1: Inintial Page](#page-1-inintial-page)
    - [Here’s how the pronouns differ based on the accent.](#heres-how-the-pronouns-differ-based-on-the-accent)
  - [Page 2: Verb Conjugation Page](#page-2-verb-conjugation-page)
    - [The following table explains how to use the most common auxiliary verbs.](#the-following-table-explains-how-to-use-the-most-common-auxiliary-verbs)
    - [The following table provides an example data representation.](#the-following-table-provides-an-example-data-representation)
- [Architecture](#architecture)
  - [The Backend](#the-backend)
  - [The Frontend](#the-frontend)
  - [Prerequisites and Requirements](#prerequisites-and-requirements)


## Description

Mastering verb conjugations in Spanish can feel overwhelming, especially with the many auxiliary verbs that form endless combinations. But here's the secret: it’s not as hard as it seems!

**Conjugator** isn’t just another tool. We’ve designed it to be as clear and user-friendly as possible, avoiding complex terms and confusing structures. It helps you not only grasp the basic forms but also understand the most common and practical combinations. And the best part? You’ll gain the confidence to create your own combinations effortlessly!

## How to Use
**Conjugator** keeps things simple - there are only two pages to navigate!

### Page 1: Inintial Page

On the first page, you can choose from three different regional accents, generalized for certain countries:

- **Con Voseo:** 🇦🇷 🇺🇾 🇵🇾 🇨🇷 🇸🇻 🇳🇮 🇭🇳  
- **Vosotros:** 🇪🇸 🇬🇶  
- **Sin Voseo:** 🇲🇽 🇨🇴 🇻🇪 🇨🇺 🇵🇪 🇨🇱 🇧🇴 🇪🇨 🇵🇦 🇩🇴 🇺🇸 🇬🇹 🇮🇨

#### Here’s how the pronouns differ based on the accent.

| **Con Voseo**           | **Vosotros**             | **Sin Voseo**          |
|-------------------------|--------------------------|------------------------|
| Yo                      | Yo                       | Yo                     |
| Vos                     | Tú                       | Tú                     |
| Él, Ella, Usted          | Él, Ella, Usted          | Él, Ella, Usted         |
| Nosotros, Nosotras       | Nosotros, Nosotras       | Nosotros, Nosotras      |
|                          | Vosotros, Vosotras       |                         |
| Ellos, Ellas, Ustedes    | Ellos, Ellas, Ustedes    | Ellos, Ellas, Ustedes   |

There's also an input field where you can type any Spanish verb — including reflexive verbs!

### Page 2: Verb Conjugation Page
On the second page, you can reveal a hidden table by clicking the button at the top.
    
#### The following table explains how to use the most common auxiliary verbs.

| Structure           | Usage    | Meaning                                                          |
|---------------------|----------|------------------------------------------------------------------|
| **Haber + participle**  |    ✓     | Indicates an action that occurred before the moment being discussed. |
|                     |    ✗     | The action only refers to a specific point in time.              |
| **Estar + gerund**      |    ✓     | Defines a process happening short-term and continuously.         |
|                     |    ✗     | Describes an instantaneous or long-term action.                  |
| **Ser + participle**    |    ✓     | Used to express the passive voice.                              |
|                     |    ✗     | Refers to the active voice.                                      |
| **Ir a + infinitive**   |    ✓     | Indicates an intention, prediction, or future action.           |
| **Poder + infinitive**  |    ✓     | Expresses the possibility of performing an action.              |
| **Deber + infinitive**  |    ✓     | Indicates obligation, desirable action, or necessity.           |

#### The following table provides an example data representation.
| Tense Name                                             | Description                                          | Scheme                                          | Use-Cases                                                       | Examples                                                                                                 |
|-------------------------------------------------------|------------------------------------------------------|-------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Futuro indicativo                                | 1: Future tense                                 | *Infinitive + "e"/"a".*                        | Promises and predictions.                                   | *Volveremos la semana que viene.*                                                                         |
|                                                       | 2: Hypothesis about the present                 |                                                 | Questioning, wondering, or hypothesizing about the present. | *¿No sabrá qué hacer? ¿Estará vivo Elvis?*|

## Architecture

### The Backend

**Conjugator** is developed in Python 3.12.6, ensuring compatibility with Python 3.10.x classes, methods, and functions.

The application is built using the Flask micro web framework and runs on the Gunicorn WSGI HTTP server.

For the database, TinyDB is used due to the relatively small number of records that need to be stored. CRUD operations are handled through custom ORM methods.

### The Frontend

The frontend uses Flask's static templates to render HTML, with static CSS files for styling.

To store data such as verb tense names, descriptions, conjugation patterns, and usage examples, TOML files are utilized. This allows for faster and simpler access by the frontend templating engine.

### Prerequisites and Requirements

To run **Conjugator**, ensure you have the following Python packages installed:

```Flask==3.0.2
Werkzeug==3.0.2
beautifulsoup4==4.12.3
requests==2.31.0
tinydb==4.8.0
tomli==2.0.1
gunicorn==20.1.0
