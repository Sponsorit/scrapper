 driver.get(link)
                    dataCollected[row[0]]["twitterLink"]=link
                    descriptionSpans = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testId='UserDescription'] span")))
                    for span in descriptionSpans:
                        spanText = span.text
                        dataCollected[row[0]]["twitterBussinesEmail"]=re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', spanText)