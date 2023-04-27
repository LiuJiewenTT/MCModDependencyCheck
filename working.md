# Working

Here is the things during my work.

[toc]

## Progress

- [x] Implement reading information from file
- [x] Implement collecting and sorting information and form a structure of information for further uses.
- [ ] Implement Dependencies Checks, including `modId`, `versionRange` and `mandatory` attributes.
  - [x] check `modId` and `mandatory`
  - [ ] check `versionRange`
- [x] Implement Document Delivery Mechanism.
- [ ] *more in the future*.



## Links

---

To manipulate jar file, I assume it is kind of zip file.
And I find module concerning zips. That is: *zipfile* module.

1. [zipfile.html](https://docs.python.org/3/library/zipfile.html)
2. [zipfile.html#zipfile-objects](https://docs.python.org/3/library/zipfile.html#zipfile-objects)
3. [zipfile.html#path-objects](https://docs.python.org/3/library/zipfile.html#path-objects)

---

## Update Logs

### 2023.4.26

1. Now there is an ability to give you the documents of itself from command line. The function is completed for use.
2. Use `-GiveDoc` option to choose document and `-DocLang` option to choose language.
3. If you use `-ChooseDoc` option you can type in the executor and options to start with. 
4. If you're using the builded version, you may need to come with `-GiveDoc_SleepExit {seconds}` or `-GiveDoc_PauseExit`. (Replace '{seconds}' with that you want it to be.
5. All should be compatible to crossing platforms.

---

### 2023.4.22

- Add option `--version`.
- Correct typo for `-forceMandatory` option.
- Try two new icons.

---

### 2023.4.17

- LICENSE is now integrated and can be view by option `-license`.
- Debug modes can be enabled through the options. But not set in codes very well until now.
- To see "About", pass option "-onlyAbout".
- Mandatory property is considered and can be configured now.

---

### 2023.2.7

Alpha version.

Basic functions are ready to use.