import React, { FC } from 'react';
import { Switch, Route } from 'react-router-dom';
import { useHistory } from 'react-router';
import { makeStyles } from '@material-ui/core/styles';

import { Home, Login, SignUp, Protected, PrivateRoute } from './views';
import { Admin } from './admin';
import { logout } from './utils/auth';

import AddProfessor from './views/AddProfessor';
import AddTA from './views/AddTA';


const useStyles = makeStyles((theme) => ({
  app: {
    textAlign: 'center',
  },
  header: {
    backgroundColor: '#282c34',
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 'calc(10px + 2vmin)',
    color: 'white',
  },
}));

export const Routes: FC = () => {
  const classes = useStyles();
  const history = useHistory();

  return (
    <Switch>
      <Route path="/admin">
        <Admin />
      </Route>

      <div className={classes.app}>
        <header className={classes.header}>
          <Route path="/login" component={Login} />
          <Route path="/signup" component={SignUp} />
          <a href="/add-professor" style={{ color: "#61dafb", marginBottom: "1em" }}>Add Professor</a>
          <a href="/add-ta" style={{ color: "#61dafb", marginBottom: "1em" }}>Add TA</a>
          <Route
            path="/logout"
            render={() => {
              logout();
              history.push('/');
              return null;
            }}
          />
          <PrivateRoute path="/protected" component={Protected} />
          <Route exact path="/" component={Home} />
          <Route path="/add-professor" component={AddProfessor} />
          <Route path="/add-ta" component={AddTA} />
        </header>
      </div>
    </Switch>
  );
};
