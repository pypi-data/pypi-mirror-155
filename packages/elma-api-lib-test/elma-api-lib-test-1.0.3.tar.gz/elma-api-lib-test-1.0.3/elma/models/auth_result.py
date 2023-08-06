class AuthResult:
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.AuthToken = data['AuthToken']
        self.SessionToken = data['SessionToken']
        self.CurrentUserId = int(data['CurrentUserId'])
        self.CurrentUserName = data['CurrentUserName']
        self.Lang = data['Lang']
