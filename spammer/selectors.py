class Selectors:
    TEXT_FIELD = '//div[contains(@class, "public-DraftEditor-content")][@role="textbox"][@data-testid="dmComposerTextInput"]'
    FILE_INPUT = '//input[contains(@accept, "image/jpeg,image/png,image/webp,image/gif")][@type="file"][@data-testid="fileInput"]'
    SUBMIT_BUTTON = '//button[@role="button"][@type="button"][@data-testid="dmComposerSendButton"]'

    CHAT_LIST = '//div[@role="tablist"]'
